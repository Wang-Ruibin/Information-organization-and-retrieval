document.addEventListener('DOMContentLoaded', () => {
    const facetsListContainer = document.getElementById('facets-list');
    const servicesListContainer = document.getElementById('services-list');
    // The context path is defined in pom.xml as <finalName>logistics</finalName>
    const apiUrl = '/logistics/api'; 

    let selectedFilters = {};

    // 1. 获取并渲染分面
    const loadFacets = async () => {
        try {
            const response = await fetch(`${apiUrl}/facets`);
            const facets = await response.json();

            facetsListContainer.innerHTML = ''; // 清空加载提示

            facets.forEach(facet => {
                const group = document.createElement('div');
                group.className = 'facet-group';

                const title = document.createElement('h3');
                title.textContent = facet.facet_name;
                group.appendChild(title);

                const list = document.createElement('ul');
                facet.values.forEach(value => {
                    const listItem = document.createElement('li');
                    const label = document.createElement('label');
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.dataset.facetCode = facet.facet_code;
                    checkbox.dataset.valueId = value.id;

                    label.appendChild(checkbox);
                    label.appendChild(document.createTextNode(value.value));
                    listItem.appendChild(label);
                    list.appendChild(listItem);
                });

                group.appendChild(list);
                facetsListContainer.appendChild(group);
            });
        } catch (error) {
            facetsListContainer.innerHTML = '<p>加载筛选条件失败，请确保后端服务已启动。</p>';
            console.error('Error loading facets:', error);
        }
    };

    // 2. 获取并渲染服务 (Updated to use GET with query parameters)
    const loadServices = async () => {
        try {
            const params = new URLSearchParams();
            for (const facetCode in selectedFilters) {
                selectedFilters[facetCode].forEach(valueId => {
                    params.append(facetCode, valueId);
                });
            }
            
            const queryString = params.toString();
            const fetchUrl = `${apiUrl}/services${queryString ? '?' + queryString : ''}`;

            const response = await fetch(fetchUrl);
            const services = await response.json();

            servicesListContainer.innerHTML = ''; // 清空

            if (services.length === 0) {
                servicesListContainer.innerHTML = '<p>没有找到符合条件的服务。</p>';
                return;
            }

            services.forEach(service => {
                const card = document.createElement('div');
                card.className = 'service-card';

                const name = document.createElement('h3');
                name.textContent = service.name;
                card.appendChild(name);

                const description = document.createElement('p');
                description.textContent = service.description;
                card.appendChild(description);

                servicesListContainer.appendChild(card);
            });
        } catch (error) {
            servicesListContainer.innerHTML = '<p>加载服务列表失败。</p>';
            console.error('Error loading services:', error);
        }
    };

    // 3. 处理筛选事件
    facetsListContainer.addEventListener('change', (event) => {
        if (event.target.type === 'checkbox') {
            const facetCode = event.target.dataset.facetCode;
            const valueId = parseInt(event.target.dataset.valueId, 10);

            if (!selectedFilters[facetCode]) {
                selectedFilters[facetCode] = [];
            }

            if (event.target.checked) {
                selectedFilters[facetCode].push(valueId);
            } else {
                selectedFilters[facetCode] = selectedFilters[facetCode].filter(id => id !== valueId);
                if (selectedFilters[facetCode].length === 0) {
                    delete selectedFilters[facetCode];
                }
            }
            
            loadServices(); // 重新加载服务
        }
    });

    // 初始化加载
    loadFacets();
    loadServices();
});