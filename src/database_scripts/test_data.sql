INSERT INTO retail_feedback.prod.user_info (id_user, id_platform, txt_userlink, txt_username)
VALUES
    ('user1', 'platform1', 'userlink1', 'username1'),
    ('user2', 'platform2', 'userlink2', 'username2');

INSERT INTO retail_feedback.prod.platform (id_platform, txt_name_platform, txt_link_main_page)
VALUES
    ('platform1', 'Platform 1 Name', 'http://platform1.com'),
    ('platform2', 'Platform 2 Name', 'http://platform2.com');

INSERT INTO retail_feedback.prod.company (id_parent_company, txt_name_company)
VALUES
    ('company1', 'Company 1 Name'),
    ('company2', 'Company 2 Name');

INSERT INTO retail_feedback.prod.store (id_store, id_parent_company, txt_address, txt_name, num_longitude, num_latitude, num_phone_number, text_web_link, flg_handicapped_accessible)
VALUES
    ('store1', 'company1', '123 Store St', 'Store 1', 12.345, 67.890, 123456789, 'http://store1.com', true),
    ('store2', 'company2', '456 Store Ave', 'Store 2', 98.765, 43.210, 987654321, 'http://store2.com', false);

INSERT INTO retail_feedback.prod.raw_json (id_feedback, txt_json)
VALUES
    ('feedback1', '{"key1": "value1"}'),
    ('feedback2', '{"key2": "value2"}');

INSERT INTO retail_feedback.prod.feedback (id_feedback, id_user, id_platform, id_store, txt_feedback, cnt_likes, cnt_dislikes, dt_feedback, num_rate, num_max_rate)
VALUES
    ('feedback1', 'user1', 'platform1', 'store1', 'This is feedback 1', 10, 2, '2023-09-08', 4.5, 5.0, true),
    ('feedback2', 'user2', 'platform2', 'store2', 'This is feedback 2', 8, 1, '2023-09-07', 3.8, 5.0, false);

INSERT INTO retail_feedback.prod.ai_responses (id_feedback, json_gpt_resp_content, dtime_update)
VALUES
    ('feedback1', '{"response1": "AI response 1"}', '2023-09-08 10:00:00'),
    ('feedback2', '{"response2": "AI response 2"}', '2023-09-07 11:00:00');

INSERT INTO retail_feedback.prod.ai_parsed_responses (id_feedback, score_overall, txt_overall, score_product_range, txt_product_range, score_staff, txt_staff, score_prices, txt_prices, score_freshness, txt_freshness, score_bonus_program, txt_bonus_program, dtime_update)
VALUES
    ('feedback1', 4.0, 'Good', 3.5, 'Average', 4.2, 'Excellent', 3.8, 'Average', 4.5, 'Excellent', 3.0, 'Fair', '2023-09-08 10:30:00'),
    ('feedback2', 3.2, 'Average', 3.0, 'Fair', 3.8, 'Average', 2.5, 'Poor', 3.7, 'Average', 2.8, 'Poor', '2023-09-07 11:30:00');

