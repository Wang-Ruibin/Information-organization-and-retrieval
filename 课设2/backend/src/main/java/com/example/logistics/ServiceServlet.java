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
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@WebServlet("/api/services")
public class ServiceServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");

        StringBuilder sql = new StringBuilder("SELECT s.id, s.name, s.description FROM services s");
        List<Object> params = new ArrayList<>();
        
        Map<String, String[]> filters = req.getParameterMap();
        if (!filters.isEmpty()) {
            sql.append(" WHERE ");
            List<String> whereClauses = new ArrayList<>();
            
            for (Map.Entry<String, String[]> entry : filters.entrySet()) {
                String facetCode = entry.getKey();
                String[] valueIds = entry.getValue();

                if (valueIds != null && valueIds.length > 0) {
                    StringBuilder placeholders = new StringBuilder();
                    for (int i = 0; i < valueIds.length; i++) {
                        placeholders.append(i == 0 ? "?" : ", ?");
                    }
                    
                    whereClauses.add("s.id IN (SELECT sfv.service_id FROM service_facet_values sfv " +
                                     "JOIN facet_values fv ON sfv.facet_value_id = fv.id " +
                                     "JOIN facets f ON fv.facet_id = f.id " +
                                     "WHERE f.code = ? AND fv.id IN (" + placeholders.toString() + "))");
                    params.add(facetCode);
                    for (String valueId : valueIds) {
                        params.add(Integer.parseInt(valueId));
                    }
                }
            }
            sql.append(String.join(" AND ", whereClauses));
        }
        
        sql.append(" ORDER BY s.id;");

        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql.toString())) {
            
            for (int i = 0; i < params.size(); i++) {
                stmt.setObject(i + 1, params.get(i));
            }

            ResultSet rs = stmt.executeQuery();
            JsonArray servicesArray = new JsonArray();

            while (rs.next()) {
                JsonObject service = new JsonObject();
                service.addProperty("id", rs.getInt("id"));
                service.addProperty("name", rs.getString("name"));
                service.addProperty("description", rs.getString("description"));
                servicesArray.add(service);
            }

            PrintWriter out = resp.getWriter();
            out.print(new Gson().toJson(servicesArray));
            out.flush();

        } catch (SQLException e) {
            e.printStackTrace();
            resp.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            resp.getWriter().write("{\"error\": \"Database error retrieving services\"}");
        } catch (NumberFormatException e) {
            e.printStackTrace();
            resp.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            resp.getWriter().write("{\"error\": \"Invalid filter value format\"}");
        }
    }
}