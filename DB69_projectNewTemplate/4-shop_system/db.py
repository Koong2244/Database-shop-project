# =======================================================================================
#  db.py — ชั้นติดต่อฐานข้อมูล  ★★★ นิสิตเขียน SQL ในไฟล์นี้ ★★★
#  มองหาคำว่า  # TODO  ทุกฟังก์ชัน — ใช้ %s เป็น placeholder เสมอ (กัน SQL injection)
# =======================================================================================
import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT)


# def run_query(sql, params=None):
#     """รัน SELECT คืนผลเป็น list ของ dict"""
#     conn = get_connection(); cur = conn.cursor(dictionary=True)
#     cur.execute(sql, params or ()); rows = cur.fetchall()
#     cur.close(); conn.close(); return rows
def run_query(sql, params=None, commit=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, params or [])
        if commit:
            conn.commit()
            return {"status": "success"}
        result = cursor.fetchall()
        return result
    except Exception as e:
        if commit:
            conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
    


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params or ()); conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close(); conn.close(); return out


def blank_to_none(value):
    """ช่องที่ไม่ได้กรอกในฟอร์มจะส่งมาเป็น "" — แปลงเป็น None (= NULL ใน SQL)
    ใช้กับคอลัมน์ที่ว่างได้ เช่น return_date, paid_date  เพราะ MySQL ไม่รับ '' เป็น DATE"""
    return None if value in ("", None) else value


def _todo(name):
    raise NotImplementedError(f"TODO: ยังไม่ได้เขียนฟังก์ชัน {name} ใน db.py")


# ---------------------------- ลูกค้า (customer) ----------------------------
# def search_customers(filters):
#     """ค้นหา ลูกค้า ตามเงื่อนไข (name, email, tier)
#     คำใบ้: เริ่มจาก sql = "SELECT * FROM customer WHERE 1=1"
#     แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
#     # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
#     _todo("search_customers")
def search_customers(filters):
    sql = "SELECT * FROM customer WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"; params.append("%" + filters["name"] + "%")

    if filters.get("email"):
        sql += " AND email LIKE %s"; params.append("%" + filters["email"] + "%")

    if filters.get("tier"):
        sql += " AND tier = %s"; params.append(filters["tier"])

    sql += " ORDER BY cust_id ASC"
    return run_query(sql, params)



# def get_customer(cust_id):
#     """ดึง ลูกค้า 1 รายการตาม cust_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
#     # TODO: SELECT * FROM customer WHERE cust_id = %s แล้วคืนแถวเดียว
#     _todo("get_customer")
def get_customer(cust_id):
    rows = run_query("SELECT * FROM customer WHERE cust_id = %s", (cust_id,))
    return rows[0] if rows else None 


# def create_customer(data):
#     """เพิ่ม ลูกค้า ใหม่ — data มีคีย์: name, email, address, tier"""
#     # TODO: INSERT INTO customer (...) VALUES (%s, ...)
#     _todo("create_customer")
def create_customer(data):
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    address = str(data.get("address", "")).strip()
    cust_type = data.get("cust_type", "normal")

    if not name:
        raise ValueError("กรุณากรอกชื่อลูกค้า")
    if not email:
        raise ValueError("กรุณากรอกอีเมลลูกค้า")
    if not address:
        raise ValueError("กรุณากรอกที่อยู่ลูกค้า")

    sql = """
        INSERT INTO customer (name, email, address, cust_type)
        VALUES (%s, %s, %s, %s)
    """
    return run_query(sql, [name, email or None, address or None, cust_type], commit=True)


# def update_customer(cust_id, data):
#     """แก้ไข ลูกค้า ตาม cust_id"""
#     # TODO: UPDATE customer SET ... WHERE cust_id=%s
#     _todo("update_customer")
def update_customer(cust_id, data):
    return run_command(
        "UPDATE customer SET name=%s, email=%s, address=%s, "
        "tier=%s WHERE cust_id=%s",
        (data["name"], data["email"], data["address"],
         data["tier"], cust_id))


# def delete_customer(cust_id):
#     """ลบ ลูกค้า ตาม cust_id"""
#     # TODO: DELETE FROM customer WHERE cust_id=%s
#     _todo("delete_customer")
def delete_customer(cust_id):
	return run_command("DELETE FROM customer WHERE cust_id=%s", (cust_id,)) 



# ---------------------------- สินค้า (product) ----------------------------
# def search_products(filters):
#     """ค้นหา สินค้า ตามเงื่อนไข (name, category)
#     คำใบ้: เริ่มจาก sql = "SELECT * FROM product WHERE 1=1"
#     แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
#     # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
#     _todo("search_products")
def search_products(filters):
    sql = "SELECT * FROM product WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"; params.append("%" + filters["name"] + "%")

    if filters.get("category"):
        sql += " AND category LIKE %s"; params.append("%" + filters["category"] + "%")

    sql += " ORDER BY product_id ASC"
    return run_query(sql, params)


# def get_product(product_id):
#     """ดึง สินค้า 1 รายการตาม product_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
#     # TODO: SELECT * FROM product WHERE product_id = %s แล้วคืนแถวเดียว
#     _todo("get_product")
def get_product(product_id):
    rows = run_query("SELECT * FROM product WHERE product_id = %s", (product_id,))
    return rows[0] if rows else None

def get_categories():
    sql = """SELECT DISTINCT category
    FROM product WHERE category IS NOT NULL
    AND category != '' 
    ORDER BY category ASC
    """
    return run_query(sql)

# def create_product(data):
#     """เพิ่ม สินค้า ใหม่ — data มีคีย์: name, category, price, stock"""
#     # TODO: INSERT INTO product (...) VALUES (%s, ...)
#     _todo("create_product")
def create_product(data):
    name = (data.get("name") or "").strip()
    if not name:
        raise ValueError("กรุณากรอกชื่อสินค้า")

    price_val = str(data.get("price", "")).strip()
    stock_val = str(data.get("stock", "")).strip()

    if price_val == "":
        raise ValueError("กรุณากรอกราคาสินค้า")
    if stock_val == "":
        raise ValueError("กรุณากรอกจำนวนสต็อก")

    try:
        price = float(price_val)
        stock = int(stock_val)
    except ValueError:
        raise ValueError("ราคาและสต็อกต้องเป็นตัวเลขเท่านั้น")

    if price < 0:
        raise ValueError("ราคาสินค้าต้องไม่เป็นค่าติดลบ")
    if stock < 0:
        raise ValueError("จำนวนสต็อกต้องไม่เป็นค่าติดลบ")

    sql = "INSERT INTO product (name, category, price, stock) VALUES (%s, %s, %s, %s)"
    return run_query(sql, [name, data.get("category"), price, stock], commit=True)


# def update_product(product_id, data):
#     """แก้ไข สินค้า ตาม product_id"""
#     # TODO: UPDATE product SET ... WHERE product_id=%s
#     _todo("update_product")
def update_product(_id, data):
    name = (data.get("name") or "").strip()
    if not name:
        raise ValueError("กรุณากรอกชื่อสินค้า")

    price_val = str(data.get("price", "")).strip()
    stock_val = str(data.get("stock", "")).strip()

    if price_val == "":
        raise ValueError("กรุณากรอกราคาสินค้า")
    if stock_val == "":
        raise ValueError("กรุณากรอกจำนวนสต็อก")

    try:
        price = float(price_val)
        stock = int(stock_val)
    except ValueError:
        raise ValueError("ราคาและสต็อกต้องเป็นตัวเลขเท่านั้น")

    if price < 0:
        raise ValueError("ราคาสินค้าต้องไม่เป็นค่าติดลบ")
    if stock < 0:
        raise ValueError("จำนวนสต็อกต้องไม่เป็นค่าติดลบ")

    sql = "UPDATE product SET name = %s, category = %s, price = %s, stock = %s WHERE product_id = %s"
    return run_query(sql, [name, data.get("category"), price, stock, _id], commit=True)


# def delete_product(product_id):
#     """ลบ สินค้า ตาม product_id"""
#     # TODO: DELETE FROM product WHERE product_id=%s
#     _todo("delete_product")
def delete_product(product_id):
	return run_command("DELETE FROM product WHERE product_id=%s", (product_id,)) 


# ------------------------ ออเดอร์ (shop_order) ---------------------------
# def search_orders(filters):
#     """ค้นหา ออเดอร์ ตามเงื่อนไข (cust_id, status)
#     ต้องแสดงคอลัมน์: order_id, cust_id, ชื่อลูกค้า, order_date, status, total (ยอดรวม)
#     คำใบ้:
#       - JOIN customer เพื่อแสดงชื่อลูกค้า
#       - total ไม่ได้เก็บเป็นคอลัมน์ → คำนวณ = SUM(qty × unit_price) จาก order_line
#         LEFT JOIN กับ subquery ที่รวมยอดของแต่ละ order_id แล้วใช้ IFNULL(..., 0)
#       - เงื่อนไขทุกตัวใช้ = %s"""
#     # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
#     _todo("search_orders")
def search_orders(filters):
    sql = """
        SELECT 
            o.order_id, 
            o.cust_id, 
            c.name AS cust_name, 
            COALESCE(GROUP_CONCAT(CONCAT(p.name, ' (x', ol.qty, ')') SEPARATOR ', '), '-') AS items_detail,
            o.coupon_code, 
            o.order_date, 
            o.status,
            COALESCE(pay.method, '-') AS payment_method,
            COALESCE(SUM(ol.qty * ol.unit_price), 0) AS total
        FROM shop_order o
        JOIN customer c ON o.cust_id = c.cust_id
        LEFT JOIN order_line ol ON o.order_id = ol.order_id
        LEFT JOIN product p ON ol.product_id = p.product_id
        LEFT JOIN payment pay ON o.order_id = pay.order_id
        WHERE 1=1
    """
    params = []
    
    # ถ้ามีการกรอกช่องค้นหาลูกค้า
    if filters.get("cust_id"):
        val = str(filters["cust_id"]).strip()
        if val.isdigit():
            # ถ้าพิมพ์มาเป็นตัวเลข ให้ค้นหาจาก cust_id
            sql += " AND o.cust_id = %s"
            params.append(int(val))
        else:
            # ถ้าพิมพ์มาเป็นข้อความ ให้ค้นหาจาก c.name
            sql += " AND c.name LIKE %s"
            params.append(f"%{val}%")

    if filters.get("status"):
        sql += " AND o.status = %s"
        params.append(filters["status"])
        
    sql += " GROUP BY o.order_id, o.cust_id, c.name, o.coupon_code, o.order_date, o.status, pay.method"
    sql += " ORDER BY o.order_id DESC"
    return run_query(sql, params)


# def get_order(order_id):
#     """ดึง ออเดอร์ 1 รายการตาม order_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
#     # TODO: SELECT * FROM shop_order WHERE order_id = %s แล้วคืนแถวเดียว
#     _todo("get_order")
def get_order(order_id):
    sql = "SELECT * FROM shop_order WHERE order_id = %s"
    res = run_query(sql, (order_id,))
    if not res:
        raise ValueError("ไม่พบข้อมูลออเดอร์")
    
    order = res[0]
    if order.get("order_date"):
        order["order_date"] = str(order["order_date"])
        
    return order

# def check_can_ship(order_id):
#     """ตรวจก่อนเปลี่ยนสถานะเป็น 'shipped' — ถ้าไม่ผ่านให้ raise ValueError("ข้อความ")
#     (หน้าเว็บจะแสดงข้อความนั้นเป็น alert ให้ผู้ใช้เห็น และไม่บันทึกข้อมูล)
#     กฎ: จัดส่งได้เฉพาะออเดอร์ที่ชำระเงินแล้ว = มีแถวในตาราง payment ของออเดอร์นี้
#        → SELECT EXISTS (SELECT 1 FROM payment WHERE order_id = %s) AS paid
#          (หรือ SELECT COUNT(*) ... ก็ได้)
#     ตัวอย่าง: raise ValueError("ออเดอร์นี้ยังไม่ได้ชำระเงิน จัดส่งไม่ได้")"""
#     # TODO: เขียนการตรวจตามคำใบ้
#     _todo("check_can_ship")
def check_can_ship(order_id):
    sql = "SELECT EXISTS (SELECT 1 FROM payment WHERE order_id = %s) AS paid"
    result = run_query(sql, (order_id,))
    
    is_paid = result[0]["paid"] if result else 0
    
    if not is_paid:
        raise ValueError("ออเดอร์นี้ยังไม่ได้ชำระเงิน จัดส่งไม่ได้")


# def create_order(data):
#     """เพิ่ม ออเดอร์ ใหม่ — data มีคีย์: cust_id, order_date, status
#     คำใบ้:
#       1) ออเดอร์ใหม่ยังไม่มีการชำระเงิน → ถ้า status = 'shipped' ให้ raise ValueError ได้เลย
#       2) INSERT INTO shop_order (...) VALUES (%s, ...)"""
#     # TODO: เขียนตามคำใบ้
#     _todo("create_order")
def create_order(data):
    # ออเดอร์สร้างใหม่จะจัดส่ง (shipped) ทันทีไม่ได้
    status = data.get("status", "pending")
    if status == "shipped":
        raise ValueError("ไม่สามารถสร้างออเดอร์ในสถานะ 'shipped' ได้เนื่องจากยังไม่มีการชำระเงิน")

    conn = get_connection()
    try:
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)

        # ตรวจสอบลูกค้า 
        cust_val = str(data["cust_id"]).strip()
        if cust_val.isdigit():
            cust_id = int(cust_val)
        else:
            cursor.execute("SELECT cust_id FROM customer WHERE name = %s", (cust_val,))
            cust_row = cursor.fetchone()
            if not cust_row:
                raise ValueError(f"ไม่พบข้อมูลลูกค้านี้: {cust_val}")
            cust_id = cust_row["cust_id"]

        # บันทึกข้อมูลลงตาราง shop_order
        sql_order = """
            INSERT INTO shop_order (cust_id, coupon_code, order_date, status)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_order, (
            cust_id,
            data.get("coupon_code") or None,
            data["order_date"],
            status
        ))
        order_id = cursor.lastrowid

        # ตรวจสอบสต็อกและบันทึกรายการสินค้า
        if data.get("product_id") and data.get("qty"):
            prod_val = str(data["product_id"]).strip()
            qty = int(data.get("qty", 1))

            if qty <= 0:
                raise ValueError("จำนวนสินค้าที่สั่งซื้อต้องมากกว่า 0 ชิ้น")

            if prod_val.isdigit():
                cursor.execute("SELECT product_id, name, price, stock FROM product WHERE product_id = %s", (int(prod_val),))
            else:
                cursor.execute("SELECT product_id, name, price, stock FROM product WHERE name = %s", (prod_val,))
            
            prod = cursor.fetchone()
            if prod:
                # ตรวจสอบว่าสินค้าในสต็อกเพียงพอหรือไม่
                if prod["stock"] < qty:
                    raise ValueError(f"สินค้า '{prod['name']}' สินค้าคงเหลือไม่พอ (เหลือเพียง {prod['stock']} ชิ้น)")

                product_id = prod["product_id"]
                unit_price = prod["price"]
                
                cursor.execute(
                    "INSERT INTO order_line (order_id, product_id, qty, unit_price) VALUES (%s, %s, %s, %s)",
                    (order_id, product_id, qty, unit_price)
                )
                cursor.execute("UPDATE product SET stock = stock - %s WHERE product_id = %s", (qty, product_id))

                # บันทึกการชำระเงิน (payment)
                if data.get("payment_method") and data["payment_method"] != "-":
                    total_amt = unit_price * qty
                    cursor.execute(
                        "INSERT INTO payment (order_id, method, amount, paid_date) VALUES (%s, %s, %s, NOW())",
                        (order_id, data["payment_method"], total_amt)
                    )

        conn.commit()
        return {"status": "success", "order_id": order_id}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


# def update_order(order_id, data):
#     """แก้ไข ออเดอร์ ตาม order_id
#     คำใบ้:
#       1) ถ้า status ใหม่ = 'shipped' → เรียก check_can_ship(order_id) ก่อน
#       2) UPDATE shop_order SET ... WHERE order_id=%s"""
#     # TODO: เขียนตามคำใบ้
#     _todo("update_order")
def update_order(order_id, data):
    if "qty" in data and data["qty"] is not None:
        try:
            qty = int(data["qty"])
            if qty <= 0:
                raise ValueError("จำนวนสินค้าที่สั่งซื้อต้องมากกว่า 0 ชิ้น")
        except (ValueError, TypeError):
            raise ValueError("จำนวนสินค้าต้องเป็นตัวเลขที่มากกว่า 0")

    cust_val = str(data.get("cust_id")).strip()
    order_date = data.get("order_date")
    status = data.get("status")

    # ตรวจสอบสถานะการจัดส่ง
    if status == "shipped":
        check_can_ship(order_id)

    if cust_val.isdigit():
        cust_id = int(cust_val)
    else:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT cust_id FROM customer WHERE name = %s", (cust_val,))
        cust_row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not cust_row:
            raise ValueError(f"ไม่พบข้อมูลลูกค้านี้: {cust_val}")
        cust_id = cust_row["cust_id"]

    # อัปเดตข้อมูลในตาราง shop_order
    sql = """
        UPDATE shop_order
        SET cust_id = %s,
            order_date = %s,
            status = %s
        WHERE order_id = %s
    """
    params = (cust_id, order_date, status, order_id)
    result = run_query(sql, params, commit=True)

    # อัปเดตจำนวนสินค้าใน order_line
    if "qty" in data and data["qty"] is not None:
        sql_line = "UPDATE order_line SET qty = %s WHERE order_id = %s"
        run_query(sql_line, (int(data["qty"]), order_id), commit=True)

    return result


# def delete_order(order_id):
#     """ลบ ออเดอร์ ตาม order_id
#     คำใบ้:
#       1) ห้ามลบออเดอร์ที่ชำระเงินแล้ว → ตรวจด้วย EXISTS (SELECT 1 FROM payment WHERE order_id = %s)
#          ถ้ามี → raise ValueError("ออเดอร์นี้ชำระเงินแล้ว ลบไม่ได้")
#       2) ลบแถวลูกใน order_line ก่อน (FK) แล้วจึง DELETE FROM shop_order WHERE order_id=%s"""
#     # TODO: เขียนตามคำใบ้
#     _todo("delete_order")
def delete_order(order_id):
    check_paid_sql = "SELECT EXISTS (SELECT 1 FROM payment WHERE order_id = %s) AS paid"
    result = run_query(check_paid_sql, (order_id,))
    is_paid = result[0]["paid"] if result else 0

    if is_paid:
        raise ValueError("ออเดอร์นี้ชำระเงินแล้ว ลบไม่ได้")

    delete_line_sql = "DELETE FROM order_line WHERE order_id = %s"
    run_query(delete_line_sql, (order_id,))

    delete_order_sql = "DELETE FROM shop_order WHERE order_id = %s"
    return run_query(delete_order_sql, (order_id,))


# ---------------------------- คูปอง (coupon) ----------------------------
def search_coupons(filters):
    sql = "SELECT coupon_code, discount_pct, discount_amt, min_spend, usage_limit, times_used, is_active, valid_from, valid_until FROM coupon WHERE 1=1"
    params = []
    
    # ค้นหาตามรหัสคูปอง
    if filters.get("code"):
        sql += " AND coupon_code LIKE %s"
        params.append("%" + filters["code"] + "%")
        
    # ค้นหาตามสถานะ
    if filters.get("is_active"):
        sql += " AND is_active = %s"
        params.append(int(filters["is_active"]))

    sql += " ORDER BY valid_from DESC, valid_until DESC"
    return run_query(sql, params)

def get_coupon(coupon_code):
    rows = run_query("SELECT * FROM coupon WHERE coupon_code = %s", (coupon_code,))
    return rows[0] if rows else None

def create_coupon(data):
    sql = """
        INSERT INTO coupon (coupon_code, discount_pct, discount_amt, min_spend, usage_limit, valid_from, valid_until)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data["coupon_code"],
        data.get("discount_pct", 0) or 0,
        data.get("discount_amt", 0) or 0,
        data.get("min_spend", 0) or 0,
        data.get("usage_limit") or None,
        data.get("valid_from") or None,
        data["valid_until"]
    )
    return run_command(sql, params)

def update_coupon(_id, data):
    discount_pct = float(data.get("discount_pct", 0) or 0)
    discount_amt = float(data.get("discount_amt", 0) or 0)
    min_spend = float(data.get("min_spend", 0) or 0)
    usage_limit = data.get("usage_limit")
    is_active = int(data.get("is_active", 1) or 0)

    # ตรวจสอบค่าติดลบก่อนบันทึกลงฐานข้อมูล
    if discount_pct < 0 or discount_amt < 0:
        raise ValueError("ส่วนลดต้องไม่เป็นค่าติดลบ")
    if min_spend < 0:
        raise ValueError("ยอดซื้อขั้นต่ำต้องไม่เป็นค่าติดลบ")
    if usage_limit is not None and usage_limit != "" and int(usage_limit) < 0:
        raise ValueError("จำกัดสิทธิ์ต้องไม่เป็นค่าติดลบ")
    if is_active < 0 or is_active > 1:
        raise ValueError("สถานะต้องเป็น 0 (ปิด) หรือ 1 (เปิด) เท่านั้น")

    sql = """
        UPDATE coupon 
        SET discount_pct = %s, discount_amt = %s, min_spend = %s, 
            usage_limit = %s, is_active = %s, valid_from = %s, valid_until = %s
        WHERE coupon_code = %s
    """
    params = [
        discount_pct,
        discount_amt,
        min_spend,
        int(usage_limit) if usage_limit is not None and usage_limit != "" else None,
        is_active,
        data.get("valid_from") if data.get("valid_from") else None,
        data.get("valid_until") if data.get("valid_until") else None,
        _id
    ]
    return run_query(sql, params, commit=True) 


def delete_coupon(coupon_code):
    return run_command("DELETE FROM coupon WHERE coupon_code=%s", (coupon_code,))

# ======================================================================
#  REPORT (รายงาน — ใช้ JOIN + GROUP BY + subquery)
#  ★ ชื่อคอลัมน์ใน SELECT จะกลายเป็นหัวตารางบนเว็บ — ใช้ AS 'ชื่อภาษาไทย' ได้
# ======================================================================

def report_summary():
    """ตัวเลขสรุปบนการ์ด dashboard — คืน dict {ชื่อการ์ด: ตัวเลข}  (1 คีย์ = 1 การ์ด)
    ตอนนี้ยังไม่ได้เขียน SQL → คืนค่า None ทุกการ์ด หน้าเว็บจึงแสดง "—" รอไว้
    ★ งานของนิสิต: เขียน SQL ตามตัวอย่างด้านล่าง (1 คอลัมน์ใน SELECT = 1 การ์ด
      ชื่อหลัง AS = ข้อความใต้ตัวเลข) แล้วลบ return {...} ชุดล่างสุดทิ้ง
    ★ การ์ด "คิดเพิ่มเอง" 2 ใบ: ตั้งชื่อการ์ดใหม่ แล้วเขียน SQL เอง
    ★ ผลรวมเงินใช้ IFNULL(SUM(...), 0) — ถ้ายังไม่มีข้อมูล SUM จะได้ NULL"""

    sql = """SELECT
                (SELECT COUNT(*) FROM customer)                          AS 'ลูกค้า',
                (SELECT COUNT(*) FROM product)                           AS 'สินค้า',
                (SELECT COUNT(*) FROM order_line)                        AS 'ออร์เดอร์',
                (SELECT COUNT(*) FROM review)                            AS 'รีวิว',
                (SELECT COUNT(*) FROM shop_order)                        AS 'ยอดขาย',
                (SELECT COUNT(*) FROM shop_order WHERE status = 'waiting') AS 'ออเดอร์รอจัดส่ง'"""
    return run_query(sql)[0]
    # TODO: ระหว่างที่ยังไม่ได้เขียน SQL คืนค่า None ให้การ์ดแสดง "—" รอไว้
    return {
        "ลูกค้า":         None,   # (SELECT COUNT(*) FROM customer)
        "สินค้า":         None,   # นับสินค้าทั้งหมด
        "ออเดอร์":        None,   # นับออเดอร์ทั้งหมด
        "รีวิว":          None,   # นับรีวิวทั้งหมด
        "คิดเพิ่มเอง 1":  None,   # ตั้งชื่อการ์ดใหม่ + เขียน SQL เอง
        "คิดเพิ่มเอง 2":  None,   # ตั้งชื่อการ์ดใหม่ + เขียน SQL เอง
    }

    
def report_best_selling():
    """📈 สินค้าขายดี (Best Sellers)
    คำใบ้: JOIN order_line→product, GROUP BY product, SUM(qty), ORDER BY DESC, LIMIT 5"""
    # TODO: เขียน SQL รายงานนี้ (เขียน JOIN แบบ explicit INNER JOIN ... ON ...)
    sql = """
        SELECT 
            p.product_id        AS 'รหัสสินค้า',
            p.name              AS 'ชื่อสินค้า',
            p.category          AS 'หมวดหมู่',
            SUM(ol.qty)         AS 'จำนวนที่ขายได้'
        FROM order_line ol
        INNER JOIN product p ON ol.product_id = p.product_id
        GROUP BY p.product_id, p.name, p.category
        ORDER BY SUM(ol.qty) DESC
        LIMIT 5
    """
    return run_query(sql)

def report_customers_above_avg():
    """🏅 ลูกค้าที่ซื้อมากกว่าค่าเฉลี่ย (Above Average)
    คำใบ้: JOIN shop_order→order_line, GROUP BY customer, HAVING SUM(qty*unit_price) > (subquery AVG)"""
    # TODO: เขียน SQL รายงานนี้ (เขียน JOIN แบบ explicit INNER JOIN ... ON ...)
    sql = """SELECT c.cust_id                    AS 'รหัสลูกค้า',
                    c.name                       AS 'ชื่อลูกค้า',
                    SUM(ol.qty * ol.unit_price)  AS 'ยอดซื้อรวม'
             FROM shop_order so
             INNER JOIN customer c ON so.cust_id = c.cust_id  #ดึงชื่อลูกค้า
             INNER JOIN order_line ol ON so.order_id = ol.order_id   #ดึงรายการสินค้าและราคา
             GROUP BY c.cust_id, c.name
             HAVING SUM(ol.qty * ol.unit_price) > (
                 SELECT AVG(total_amount)  
                 FROM (
                     SELECT SUM(ol2.qty * ol2.unit_price) AS total_amount
                     FROM shop_order so2
                     INNER JOIN order_line ol2 ON so2.order_id = ol2.order_id
                     GROUP BY so2.cust_id) AS subquery)
             ORDER BY SUM(ol.qty * ol.unit_price) DESC"""
    return run_query(sql)

def report_high_rated():
    """⭐ สินค้าคะแนนรีวิวเฉลี่ย ≥ 4 (HAVING)"""
    
    sql = """
    SELECT 		 p.product_id 		    AS 'รหัสสินค้า',
           	     p.name 				AS 'ชื่อสินค้า',
    		    ROUND(AVG(r.rating), 2) AS 'คะแนนเฉลี่ย',
                COUNT(r.comment) AS 'จำนวนรีวิว'
        FROM review r
        INNER JOIN product p ON r.product_id = p.product_id   #ตารางสินค้า
        GROUP BY p.product_id, p.name
        HAVING AVG(r.rating) >= 4
        ORDER BY คะแนนเฉลี่ย DESC"""
    return run_query(sql)


def report_sales_by_category():
    """📊 ยอดขายและจำนวนสินค้าขายได้ แยกตามหมวดหมู่สินค้า (Custom Report)"""
    sql = """
        SELECT
            p.category AS 'หมวดหมู่สินค้า',
            COUNT(DISTINCT p.product_id) AS 'จำนวนรายการสินค้า',
            IFNULL(SUM(ol.qty), 0) AS 'จำนวนที่ขายได้ (ชิ้น)',
            IFNULL(SUM(ol.qty * ol.unit_price), 0) AS 'ยอดขายรวม (บาท)'
        FROM product p
        LEFT JOIN order_line ol ON p.product_id = ol.product_id
        GROUP BY p.category
        ORDER BY 'ยอดขายรวม (บาท)' DESC
    """
    return run_query(sql)

# ======================================================================
#  รายการรายงานที่แสดงบนหน้า /report  (เรียงตามลำดับที่แสดง)
#  ★ วิธีเพิ่มรายงานใหม่ (ไม่ต้องแก้ไฟล์อื่น):
#    1) เขียนฟังก์ชัน report_xxx() ด้านบน ให้ return run_query(sql)
#    2) เพิ่ม 1 บรรทัดในรายการนี้:  ("ชื่อใน-url", "หัวข้อที่แสดง", ชื่อฟังก์ชัน)
#  ★ รายการนี้ต้องอยู่ท้ายไฟล์ (หลังฟังก์ชันทั้งหมด) ไม่งั้น Python หาชื่อฟังก์ชันไม่เจอ
#  ★ ห้ามตั้งชื่อ url ว่า "summary" (ใช้แล้วสำหรับการ์ดสรุป)
# ======================================================================
REPORTS = [
    ("best-selling",    "📈 สินค้าขายดี (Best Sellers)",            report_best_selling),
    ("top-customers",   "🏅 ลูกค้าที่ซื้อมากกว่าค่าเฉลี่ย (Above Average)", report_customers_above_avg),
    ("high-rated",      "⭐ สินค้าคะแนนรีวิวเฉลี่ย ≥ 4 (HAVING)",           report_high_rated),
    ("sales-by-category", "📊 ยอดขายตามหมวดหมู่ (Custom Report)",   report_sales_by_category)  # <--- ลบเครื่องหมาย , ด้านหลังออก
]