-- ============================================================
--  schema.sql — ร้านค้าออนไลน์ (นิสิตออกแบบและเขียนเอง)
--  กติกา: 1 ออเดอร์มีหลายสินค้า (M:N: order × product ผ่าน order_line),
--         รีวิว = M:N (customer × product), การชำระเงิน 1:M จาก shop_order
-- ============================================================

-- DROP TABLE IF EXISTS payment;
-- DROP TABLE IF EXISTS review;
-- DROP TABLE IF EXISTS order_line;
-- DROP TABLE IF EXISTS shop_order;
-- DROP TABLE IF EXISTS product;
-- DROP TABLE IF EXISTS customer;

-- DROP TABLE IF EXISTS payment, review, order_line, shop_order, product, customer; 


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
constraint	cust_id_fk			foreign key (cust_id)	references customer(cust_id)	ON DELETE CASCADE
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












