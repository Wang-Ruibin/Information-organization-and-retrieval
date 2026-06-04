-- 为物流服务分面分类系统填充示例数据 (MySQL)

-- 1. 填充分面定义表 (facets)
INSERT INTO `facets` (`name`, `code`) VALUES
('服务类型', 'service_type'),
('运输方式', 'transport_mode'),
('时效', 'timeliness'),
('目的地范围', 'destination_scope'),
('特色服务', 'special_service');

-- 2. 填充分面值表 (facet_values)
-- 服务类型
INSERT INTO `facet_values` (`facet_id`, `value`) VALUES
(1, '快递'), (1, '零担'), (1, '整车');

-- 运输方式
INSERT INTO `facet_values` (`facet_id`, `value`) VALUES
(2, '陆运'), (2, '空运'), (2, '海运');

-- 时效
INSERT INTO `facet_values` (`facet_id`, `value`) VALUES
(3, '经济型'), (3, '标准型'), (3, '加急型');

-- 目的地范围
INSERT INTO `facet_values` (`facet_id`, `value`) VALUES
(4, '同城'), (4, '国内'), (4, '国际');

-- 特色服务
INSERT INTO `facet_values` (`facet_id`, `value`) VALUES
(5, '冷链'), (5, '危险品'), (5, '代收货款'), (5, '无');

-- 3. 填充物流服务产品表 (services)
INSERT INTO `services` (`id`, `name`, `description`) VALUES
(1, '顺丰标快', '快速、稳定的国内快递服务，覆盖范围广。'),
(2, '德邦零担', '专业的大件货物零担运输服务，提供门到门配送。'),
(3, '中远海运整箱', '提供标准集装箱的国际海运整箱服务。'),
(4, '京东冷链同城配', '为生鲜、医药等提供专业的同城温控配送服务。'),
(5, '跨越速运', '专注于企业用户的国内限时空运服务。');

-- 4. 填充服务-分面值关联表 (service_facet_values)
-- 将每个服务与其对应的分面值关联起来

-- 服务1: 顺丰标快 (快递, 陆运/空运, 标准型, 国内, 代收货款)
-- facet_value_ids: 1, 4, 5, 8, 11, 15
INSERT INTO `service_facet_values` (`service_id`, `facet_value_id`) VALUES
(1, 1), (1, 4), (1, 5), (1, 8), (1, 11), (1, 15);

-- 服务2: 德邦零担 (零担, 陆运, 标准型, 国内, 无)
-- facet_value_ids: 2, 4, 8, 11, 16
INSERT INTO `service_facet_values` (`service_id`, `facet_value_id`) VALUES
(2, 2), (2, 4), (2, 8), (2, 11), (2, 16);

-- 服务3: 中远海运整箱 (整车, 海运, 经济型, 国际, 无)
-- facet_value_ids: 3, 6, 7, 12, 16
INSERT INTO `service_facet_values` (`service_id`, `facet_value_id`) VALUES
(3, 3), (3, 6), (3, 7), (3, 12), (3, 16);

-- 服务4: 京东冷链同城配 (快递, 陆运, 加急型, 同城, 冷链)
-- facet_value_ids: 1, 4, 9, 10, 13
INSERT INTO `service_facet_values` (`service_id`, `facet_value_id`) VALUES
(4, 1), (4, 4), (4, 9), (4, 10), (4, 13);

-- 服务5: 跨越速运 (快递, 空运, 加急型, 国内, 无)
-- facet_value_ids: 1, 5, 9, 11, 16
INSERT INTO `service_facet_values` (`service_id`, `facet_value_id`) VALUES
(5, 1), (5, 5), (5, 9), (5, 11), (5, 16);