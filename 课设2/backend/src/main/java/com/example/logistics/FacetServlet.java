package com.example.logistics;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

@WebServlet("/api/facets")
public class FacetServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");

        String sql = "SELECT f.id as facet_id, f.name as facet_name, f.code as facet_code, " +
                     "fv.id as value_id, fv.value as value_text " +
                     "FROM facets f JOIN facet_values fv ON f.id = fv.facet_id ORDER BY f.id, fv.id";

        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            JsonArray facetsArray = new JsonArray();
            JsonObject currentFacet = null;
            int lastFacetId = -1;

            while (rs.next()) {
                int facetId = rs.getInt("facet_id");
                if (facetId != lastFacetId) {
                    if (currentFacet != null) {
                        facetsArray.add(currentFacet);
                    }
                    currentFacet = new JsonObject();
                    currentFacet.addProperty("facet_id", facetId);
                    currentFacet.addProperty("facet_name", rs.getString("facet_name"));
                    currentFacet.addProperty("facet_code", rs.getString("facet_code"));
                    currentFacet.add("values", new JsonArray());
                    lastFacetId = facetId;
                }
                
                JsonObject facetValue = new JsonObject();
                facetValue.addProperty("id", rs.getInt("value_id"));
                facetValue.addProperty("value", rs.getString("value_text"));
                currentFacet.getAsJsonArray("values").add(facetValue);
            }
            if (currentFacet != null) {
                facetsArray.add(currentFacet);
            }

            PrintWriter out = resp.getWriter();
            out.print(new Gson().toJson(facetsArray));
            out.flush();

        } catch (SQLException e) {
            e.printStackTrace();
            resp.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            resp.getWriter().write("{\"error\": \"Database error retrieving facets\"}");
        }
    }
}