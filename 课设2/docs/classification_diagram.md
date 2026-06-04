# 物流服务分面分类表 - 图形表示

下图使用 Mermaid.js 流程图展示了为物流服务设计的五个核心分面及其各自的取值。

```mermaid
graph TD
    subgraph FACETED CLASSIFICATION
        A[物流服务] --> B{服务类型};
        A --> C{运输方式};
        A --> D{时效};
        A --> E{目的地范围};
        A --> F{特色服务};

        subgraph Service Type
            B --> B1[快递];
            B --> B2[零担];
            B --> B3[整车];
        end

        subgraph Transport Mode
            C --> C1[陆运];
            C --> C2[空运];
            C --> C3[海运];
        end

        subgraph Timeliness
            D --> D1[经济型];
            D --> D2[标准型];
            D --> D3[加急型];
        end

        subgraph Destination Scope
            E --> E1[同城];
            E --> E2[国内];
            E --> E3[国际];
        end

        subgraph Special Service
            F --> F1[冷链];
            F --> F2[危险品];
            F --> F3[代收货款];
            F --> F4[无];
        end
    end

    style A fill:#333,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#555,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#555,stroke:#fff,stroke-width:2px,color:#fff
    style D fill:#555,stroke:#fff,stroke-width:2px,color:#fff
    style E fill:#555,stroke:#fff,stroke-width:2px,color:#fff
    style F fill:#555,stroke:#fff,stroke-width:2px,color:#fff
```

## 图表示例说明

上图定义了物流服务的主要分类维度。一个具体的物流服务产品可以被描述为这些分面值的组合。

例如：

- **服务产品1**:
  - **服务类型**: 零担
  - **运输方式**: 陆运
  - **时效**: 标准型
  - **目的地范围**: 国内
  - **特色服务**: 无

- **服务产品2**:
  - **服务类型**: 快递
  - **运输方式**: 空运
  - **时效**: 加急型
  - **目的地范围**: 国际
  - **特色服务**: 代收货款