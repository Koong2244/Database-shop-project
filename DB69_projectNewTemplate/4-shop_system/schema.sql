-- -- ============================================================
-- --  schema.sql — ร้านค้าออนไลน์ (นิสิตออกแบบและเขียนเอง)
-- --  กติกา: 1 ออเดอร์มีหลายสินค้า (M:N: order × product ผ่าน order_line),
-- --         รีวิว = M:N (customer × product), การชำระเงิน 1:M จาก shop_order
-- -- ============================================================
-- CREATE TABLE customer (
--     cust_id INT AUTO_INCREMENT PRIMARY KEY
--     -- TODO: name, email, address, tier
-- );
-- CREATE TABLE product (
--     product_id INT AUTO_INCREMENT PRIMARY KEY
--     -- TODO: name, category, price, stock
-- );
-- CREATE TABLE shop_order (
--     order_id INT AUTO_INCREMENT PRIMARY KEY
--     -- TODO: cust_id (FK), order_date, status ENUM('pending','shipped')
--     -- ★ ไม่ต้องมีคอลัมน์ยอดรวม — คำนวณจาก order_line (ดู search_orders ใน db.py)
-- );
-- CREATE TABLE order_line (         -- M:N: shop_order × product
--     -- TODO: order_id (FK), product_id (FK), qty, unit_price ; PRIMARY KEY (order_id, product_id)
--     order_id INT, product_id INT
-- );
-- CREATE TABLE review (             -- M:N: customer × product
--     -- TODO: cust_id (FK), product_id (FK), rating, comment, review_date ; PRIMARY KEY (cust_id, product_id)
--     cust_id INT, product_id INT
-- );
-- CREATE TABLE payment (            -- 1:M จาก shop_order
--     payment_id INT AUTO_INCREMENT PRIMARY KEY
--     -- TODO: order_id (FK), method, amount, paid_date
-- );
-- -- TODO: INSERT ข้อมูลตัวอย่างทุกตาราง
-- --   ★ ควรมีทั้งออเดอร์ที่ชำระเงินแล้ว (มีแถวใน payment) และที่ยังไม่ชำระ ไว้ทดสอบการจัดส่ง/การลบ



-- ********************************** customer **********************************

-- CREATE TABLE customer (
--     cust_id INT AUTO_INCREMENT PRIMARY KEY
--     -- TODO: name, email, address, tier);
create table customer (
		cust_id		int   AUTO_INCREMENT,
		name		varchar(100)	NOT NULL,
		email       varchar(120) NOT NULL UNIQUE,
		address		TEXT,
		tier		varchar(50)	DEFAULT  'normal',
constraint 	cust_pk		primary key (cust_id),
constraint	cust_tier_chk CHECK (LOWER(tier) IN ('normal', 'gold', 'vip', 'standard'))
);

-- ********************************** product **********************************

-- CREATE TABLE product (         1:M (Self-Referencing)
--     product_id INT AUTO_INCREMENT PRIMARY KEY
--     -- TODO: name, category, price, stock

create table product (
		product_id			int   AUTO_INCREMENT,
		name				varchar(50)	NOT NULL,
		category       		varchar(50),
		price				decimal(10,2) NOT NULL,
		stock				int NOT NULL DEFAULT 0,
constraint 	product_id_pk		primary key (product_id),
constraint	prod_price_chk		check (price >= 0),
constraint	prod_stock_chk		check (stock >= 0)
);

-- ********************************** shop_order **********************************

-- CREATE TABLE shop_order (    1:M
--     order_id INT AUTO_INCREMENT PRIMARY KEY
--     -- TODO: cust_id (FK), order_date, status ENUM('pending','shipped')
--     -- ★ ไม่ต้องมีคอลัมน์ยอดรวม — คำนวณจาก order_line (ดู search_orders ใน db.py
create table shop_order (
		order_id 		int  AUTO_INCREMENT,
		cust_id			int  NOT NULL,
		coupon_code		varchar(20) NULL, 
		order_date		DATE NOT NULL,
		status			ENUM('pending', 'waiting', 'paid', 'shipped', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
constraint 	order_id_pk			primary key (order_id),	
constraint	cust_id_fk			foreign key (cust_id)	    references customer(cust_id)	ON DELETE CASCADE,
constraint  order_coupon_fk     foreign key (coupon_code)   references coupon(coupon_code)  ON DELETE SET NULL
);


-- ********************************** order_line **********************************

-- CREATE TABLE order_line (         -- M:N: shop_order × product
-- TODO: order_id (FK), product_id (FK), qty, unit_price ; PRIMARY KEY (order_id, product_id)
-- order_id INT, product_id INT
create table	order_line (
		order_id 		int   NOT NULL,
		product_id		int   NOT NULL,
		qty				int   NOT NULL,
		unit_price		decimal(10,2) NOT NULL,
constraint 	order_line_pk		primary key (order_id, product_id),	
constraint	order_id_fk			foreign key (order_id)		references shop_order(order_id)		ON DELETE CASCADE,
constraint	product_id_fk		foreign key (product_id)	references product(product_id)		ON DELETE CASCADE,
constraint	qty_chk				check (qty > 0),
constraint 	price_chk     		check (unit_price >= 0)
);


-- ********************************** review **********************************

-- CREATE TABLE review (             -- M:N: customer × product
--     -- TODO: cust_id (FK), product_id (FK), rating, comment, review_date ; PRIMARY KEY (cust_id, product_id)
--     cust_id INT, product_id INT
create table review (
    cust_id     int NOT NULL,
    product_id  int NOT NULL,
    rating      int NOT null,
    comment     TEXT,
    review_date DATE NOT NULL,
constraint review_pk 			primary key (cust_id, product_id),
constraint review_cust_fk 		foreign key (cust_id) references customer(cust_id)			ON DELETE CASCADE,    
constraint review_prod_fk 		foreign key (product_id) references product(product_id)		ON DELETE CASCADE,  
constraint review_rating_chk 	check (rating between 1 and 5)
);


-- ********************************** payment **********************************

-- CREATE TABLE payment (            -- 1:M จาก shop_order
--     payment_id INT AUTO_INCREMENT PRIMARY KEY
-- TODO: order_id (FK), method, amount, paid_date
create table payment (
    payment_id  int AUTO_INCREMENT,
    order_id    int NOT NULL	UNIQUE,
    method      varchar(50)	NOT NULL,
    amount      decimal(10,2) NOT NULL,
    paid_date   DATETIME NOT NULL,
constraint 	payment_id_pk		primary key (payment_id),
constraint	payment_order_uniq UNIQUE (order_id), 
constraint 	payment_order_fk 	foreign key (order_id) references shop_order(order_id)	 ON DELETE CASCADE,
constraint 	payment_amt_chk  	check (amount >= 0)
);


-- ********************************** coupon **********************************
CREATE TABLE coupon (
    coupon_code     VARCHAR(20),   -- ชื่อcoupon
    discount_pct    DECIMAL(5,2)  DEFAULT 0, -- ส่วนลดเป็น %
    discount_amt    DECIMAL(10,2) DEFAULT 0, -- ส่วนลดเป็น บาท
    min_spend       DECIMAL(10,2) DEFAULT 0, -- ขั้นต่ำ
    usage_limit     INT DEFAULT NULL, -- จำนวนสิทธิ์ที่ใช้ได้
    times_used      INT DEFAULT 0,	-- จำนวนที่คูปองเคยถูกใช้
    is_active       BOOLEAN DEFAULT TRUE, -- สถานะการทำงานใช้ได้ true ใช้ไม่ได้ false
    valid_from      DATE, 				-- วันเริ่ม
    valid_until     DATE NOT NULL,		-- วันหมดหมดอายุ
constraint coupon_pk        primary key (coupon_code),
constraint coupon_pct_chk   check (discount_pct between 0 and 100),
constraint coupon_amt_chk   check (discount_amt >= 0),
constraint coupon_spend_chk check (min_spend >= 0),
constraint coupon_used_chk  check (times_used >= 0)
);


-- ============================================================
-- Complete INSERT Data
-- ============================================================

-- INSERT customer 
INSERT INTO customer (name, email, address, tier) VALUES
('Somchai Jaidee', 'somchai.j@gmail.com', '123/45 ถนนมิตรภาพ อ.เมือง จ.ขอนแก่น 40000', 'normal'),
('Somsri Saengchan', 'somsri.s@hotmail.com', '88/9 หมู่ 2 ต.ขามเรียง อ.กันทรวิชัย จ.มหาสารคาม 44150', 'gold'),
('Anan Pattana', 'anan.p@yahoo.com', '55/12 ถนนแจ้งสนิท อ.เมือง จ.ร้อยเอ็ด 45000', 'vip'),
('Kanya Wongsuwan', 'kanya.w@gmail.com', '101/3 ซอยสุขุมวิท 21 แขวงคลองเตยเหนือ เขตวัฒนา กรุงเทพฯ 10110', 'standard'),
('Nattapong Suksamran', 'nattapong.s@outlook.com', '12/4 ถนนถีนานนท์ อ.เมือง จ.กาฬสินธุ์ 46000', 'normal'),
('Pornthip Boonmee', 'pornthip.b@gmail.com', '77/3 หมู่ 5 ต.นาสีนวน อ.เมือง จ.มุกดาหาร 49000', 'gold'),
('Wichai Rattana', 'wichai.r@gmail.com', '456/8 ถนนสุรนารายณ์ อ.เมือง จ.นครราชสีมา 30000', 'vip'),
('Chutima Malee', 'chutima.m@hotmail.com', '23/1 หมู่ 8 ต.ท่าขอนยาง อ.กันทรวิชัย จ.มหาสารคาม 44150', 'standard'),
('Prasert Kaewmanee', 'prasert.k@gmail.com', '99/4 ถนนศรีจันทร์ อ.เมือง จ.ขอนแก่น 40000', 'normal'),
('Nipaporn Saelim', 'nipaporn.s@gmail.com', '34/2 ถนนชยางกูร อ.เมือง จ.อุบลราชธานี 34000', 'gold'),
('Thanakorn Sriwichai', 'thanakorn.s@outlook.com', '15/7 ถนนห้วยแก้ว อ.เมือง จ.เชียงใหม่ 50200', 'vip'),
('Ubonrat Charoenket', 'ubonrat.c@gmail.com', '88/1 ถนนพหลโยธิน อ.เมือง จ.เชียงราย 57000', 'standard'),
('Kitti Songsang', 'kitti.s@yahoo.com', '202/5 ถนนสุขุมวิท อ.เมือง จ.ชลบุรี 20000', 'normal'),
('Rattana Phetchabun', 'rattana.p@gmail.com', '67/9 ถนนเพชรเกษม อ.หาดใหญ่ จ.สงขลา 90110', 'gold'),
('Siriporn Thongyoi', 'siriporn.t@hotmail.com', '11/3 ถนนนเรศวร อ.เมือง จ.พิษณุโลก 65000', 'vip');

-- INSERT product 
INSERT INTO product (product_id, name, category, price, stock) VALUES
(1, 'Wireless Mouse', 'Electronics', 450.00, 50),
(2, 'Gaming Mouse RGB', 'Electronics', 890.00, 30),
(3, 'Mechanical Keyboard', 'Electronics', 1590.00, 20),
(4, 'Cotton T-Shirt Black', 'Apparel', 250.00, 100),
(5, 'Cotton T-Shirt White', 'Apparel', 250.00, 80),
(6, 'Denim Jacket Classic', 'Apparel', 1200.00, 15),
(7, 'Stainless Steel Water Bottle', 'Home & Living', 390.00, 40),
(8, 'Ergonomic Cushion', 'Home & Living', 550.00, 25),
(9, 'Face Moisturizer Cream', 'Beauty & Personal Care', 420.00, 60),
(10, 'Sunscreen Lotion SPF50', 'Beauty & Personal Care', 350.00, 45),
(11, 'Instant Arabica Coffee Powder', 'Food & Beverages', 180.00, 120),
(12, 'Green Tea Matcha Powder', 'Food & Beverages', 290.00, 90),
(13, 'A5 Grid Notebook', 'Books & Stationery', 85.00, 150),
(14, 'Gel Ink Pen Set 0.5mm', 'Books & Stationery', 120.00, 200),
(15, 'Yoga Mat 6mm Non-Slip', 'Sports & Outdoors', 650.00, 35);


-- INSERT shop_order
INSERT INTO shop_order (order_id, cust_id, coupon_code, order_date, status) VALUES
(1, 1, 'SPECIAL50', '2026-08-01', 'completed'),
(2, 2, 'SAVE100', '2026-08-03', 'completed'),
(3, 3, NULL, '2026-08-05', 'shipped'),
(4, 4, 'SPECIAL50', '2026-08-08', 'paid'),
(5, 5, NULL, '2026-08-10', 'waiting'),
(6, 6, NULL, '2026-08-12', 'pending'),
(7, 7, NULL, '2026-08-15', 'cancelled'),
(8, 8, NULL, '2026-08-18', 'completed'),
(9, 9, NULL, '2026-08-20', 'shipped'),
(10, 10, NULL, '2026-08-22', 'paid'),
(11, 11, NULL, '2026-08-25', 'waiting'),
(12, 12, NULL, '2026-08-28', 'pending'),
(13, 13, NULL, '2026-09-01', 'completed'),
(14, 14, NULL, '2026-09-03', 'cancelled'),
(15, 15, NULL, '2026-09-05', 'shipped');

-- INSERT order_line
INSERT INTO order_line (order_id, product_id, qty, unit_price) VALUES
(1, 1, 2, 450.00),
(1, 3, 1, 1590.00),
(2, 4, 3, 250.00),
(3, 6, 1, 1200.00),
(4, 7, 2, 390.00),
(5, 9, 1, 420.00),
(6, 11, 4, 180.00),
(7, 13, 5, 85.00),
(8, 2, 1, 890.00),
(8, 15, 1, 650.00),
(9, 5, 2, 250.00),
(10, 8, 1, 550.00),
(11, 10, 2, 350.00),
(12, 12, 1, 290.00),
(13, 14, 3, 120.00);

-- INSERT review 
INSERT INTO review (cust_id, product_id, rating, comment, review_date) VALUES
(1, 1, 5, 'คุ้มค่าสมราคา เมาส์ตอบสนองไว ลื่นไหลมากครับ', '2026-08-05'),
(1, 3, 4, 'คีย์บอร์ดวัสดุดี งานประกอบแน่น กดมันมือมาก', '2026-08-05'),
(2, 4, 5, 'ผ้านุ่มใส่สบาย ไม่ร้อนเลย จัดส่งรวดเร็ว', '2026-08-07'),
(3, 6, 4, 'เสื้อแจ็คเก็ตทรงสวย ผ้าหนาพอดีๆ ตรงปกครับ', '2026-08-10'),
(4, 7, 5, 'เก็บความเย็นได้นานทั้งวัน น้ำแข็งอยู่ข้ามคืนเลย', '2026-08-12'),
(8, 2, 5, 'ไฟ RGB สวยงามมาก เมาส์จับถนัดมือ เล่นเกมฟินสุดๆ', '2026-08-22'),
(8, 15, 4, 'แผ่นเล่นโยคะหนากำลังดี ไม่ลื่นตอนออกกำลังกาย', '2026-08-22'),
(9, 5, 3, 'คุณภาพเสื้อพอใช้ได้ ผ้าค่อนข้างบางไปหน่อย', '2026-08-24'),
(10, 8, 5, 'หมอนรองนั่งช่วยลดอาการปวดหลังได้เยอะมาก แนะนำเลยครับ', '2026-08-26'),
(13, 14, 4, 'ปากกาลื่นดี หมึกไม่ขาดสาย เขียนเพลิน', '2026-09-04'),
(5, 9, 2, 'รู้สึกยังไม่ค่อยเข้ากับสภาพผิวเท่าไหร่ ใช้แล้วแอบเหนอะ', '2026-08-15'),
(6, 11, 5, 'กาแฟหอมเข้มข้น รสชาติดี เดี๋ยวกลับมาอุดหนุนอีกแน่นอน', '2026-08-16'),
(7, 13, 1, 'กระดาษค่อนข้างบาง เขียนปากกาหมึกซึมแล้วทะลุไปอีกฝั่ง', '2026-08-18'),
(11, 10, 4, 'กันแดดเนื้อบางเบา ซึมไว ไม่เหนียวเหนอะหนะ', '2026-08-30'),
(12, 12, 5, 'ชาเขียวมัทฉะแท้ กลิ่นหอมเข้มข้น ชงใส่นมอร่อยมาก', '2026-09-01');

-- INSERT payment 
INSERT INTO payment (order_id, method, amount, paid_date) VALUES
(1, 'Credit Card', 2490.00, '2026-08-01 10:15:00'),
(2, 'PromptPay', 750.00, '2026-08-03 14:30:00'),
(3, 'Bank Transfer', 1200.00, '2026-08-05 09:20:00'),
(4, 'PromptPay', 780.00, '2026-08-08 11:45:00'),
(8, 'Credit Card', 1540.00, '2026-08-18 16:00:00'),
(9, 'Credit Card', 500.00, '2026-08-20 13:10:00'),
(10, 'PromptPay', 550.00, '2026-08-22 18:25:00'),
(13, 'PromptPay', 360.00, '2026-09-01 08:50:00'),
(15, 'Bank Transfer', 650.00, '2026-09-05 12:05:00');

-- INSERT coupon
INSERT INTO coupon (coupon_code, discount_pct, discount_amt, min_spend, usage_limit, times_used, is_active, valid_from, valid_until) VALUES 
('NEWYEAR10', 10.00, 0.00, 500.00, NULL, 0, TRUE, '2026-12-01', '2027-01-31'),
('SAVE100', 0.00, 100.00, 1000.00, 50, 0, TRUE, '2026-10-01', '2026-10-31'),
('SPECIAL50', 0.00, 50.00, 0.00, 100, 15, TRUE, '2026-09-01', '2026-12-31'),
('BROKENCODE', 20.00, 0.00, 2000.00, 500, 10, FALSE, '2026-01-01', '2026-12-31'),
('MEGA1111', 11.00, 0.00, 1111.00, 1111, 0, TRUE, '2026-11-11', '2026-11-12');


