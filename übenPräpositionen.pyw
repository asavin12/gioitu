import random
import time
import tkinter as tk
from tkinter import messagebox
import logging
import os
import sqlite3
from datetime import datetime, timedelta
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import json
import re

# Thiết lập logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Đọc API keys từ config.json
CONFIG_FILE = "config.json"

try:
    if not os.path.exists(CONFIG_FILE):
        logger.error(f"File {CONFIG_FILE} không tồn tại")
        raise FileNotFoundError(f"File {CONFIG_FILE} không tồn tại")
    
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        API_KEYS = config.get('api_keys', [])
    
    if not API_KEYS:
        logger.error("Danh sách api_keys trong config.json trống")
        raise ValueError("Danh sách api_keys trong config.json trống")
    
    logger.info(f"Đã tải {len(API_KEYS)} API keys từ config.json")
except Exception as e:
    logger.error(f"Lỗi khi đọc file config.json: {str(e)}")
    raise

# Biến toàn cục
MAX_RETRIES_PER_KEY = 3
MAX_ATTEMPTS = len(API_KEYS)

# Dữ liệu quy tắc giới từ
akkusativ_prepositions = [
    {"prep": "durch", "usage": "chỉ hướng xuyên qua một không gian hoặc nơi chốn", "reason": "Giới từ 'durch' đi với Akkusativ, thường chỉ hướng xuyên qua một không gian hoặc nơi chốn, ví dụ: 'durch den Park' (qua công viên)."},
    {"prep": "durch", "usage": "chỉ sự thông qua một phương tiện hoặc cách thức", "reason": "Giới từ 'durch' đi với Akkusativ, chỉ sự thông qua một phương tiện hoặc cách thức, ví dụ: 'durch das Telefon' (qua điện thoại)."},
    {"prep": "für", "usage": "dành cho ai đó", "reason": "Giới từ 'für' đi với Akkusativ, mang ý nghĩa dành cho một người, ví dụ: 'für dich' (cho bạn)."},
    {"prep": "für", "usage": "mục đích", "reason": "Giới từ 'für' đi với Akkusativ, chỉ mục đích của hành động, ví dụ: 'für die Reise' (cho chuyến đi)."},
    {"prep": "für", "usage": "thời gian", "reason": "Giới từ 'für' đi với Akkusativ, chỉ khoảng thời gian cụ thể, ví dụ: 'für eine Woche' (trong một tuần)."},
    {"prep": "gegen", "usage": "chỉ sự đối kháng hoặc chống lại", "reason": "Giới từ 'gegen' đi với Akkusativ, chỉ sự đối kháng hoặc chống lại, ví dụ: 'gegen den Wind' (chống lại cơn gió)."},
    {"prep": "gegen", "usage": "chỉ hướng đến về thời gian hoặc không gian", "reason": "Giới từ 'gegen' đi với Akkusativ, chỉ hướng đến về thời gian hoặc không gian, ví dụ: 'gegen Abend' (vào buổi tối)."},
    {"prep": "ohne", "usage": "chỉ sự thiếu vắng", "reason": "Giới từ 'ohne' đi với Akkusativ, chỉ sự thiếu vắng ai đó hoặc cái gì đó, ví dụ: 'ohne mein Gepäck' (không có hành lý)."},
    {"prep": "um", "usage": "chỉ vị trí xung quanh một vật", "reason": "Giới từ 'um' đi với Akkusativ, chỉ vị trí xung quanh một vật, ví dụ: 'um den Tisch' (quanh cái bàn)."},
    {"prep": "um", "usage": "chỉ thời gian cụ thể", "reason": "Giới từ 'um' đi với Akkusativ, chỉ thời gian cụ thể, ví dụ: 'um drei Uhr' (lúc 3 giờ)."},
    {"prep": "um", "usage": "chỉ sự thay đổi hoặc chuyển đổi", "reason": "Giới từ 'um' đi với Akkusativ, chỉ sự thay đổi hoặc chuyển đổi, ví dụ: 'um ein Ticket' (để đổi lấy vé)."}
]

dativ_prepositions = [
    {"prep": "aus", "usage": "chỉ nguồn gốc hoặc xuất xứ", "reason": "Giới từ 'aus' đi với Dativ, chỉ nguồn gốc hoặc xuất xứ, ví dụ: 'aus Deutschland' (từ Đức)."},
    {"prep": "aus", "usage": "chỉ hành động ra khỏi một nơi", "reason": "Giới từ 'aus' đi với Dativ, chỉ hành động ra khỏi một nơi, ví dụ: 'aus dem Haus' (ra khỏi nhà)."},
    {"prep": "bei", "usage": "chỉ vị trí gần một người", "reason": "Giới từ 'bei' đi với Dativ, chỉ vị trí gần một người, ví dụ: 'bei meiner Freundin' (ở chỗ bạn gái tôi)."},
    {"prep": "bei", "usage": "chỉ thời điểm hoặc sự kiện", "reason": "Giới từ 'bei' đi với Dativ, chỉ thời điểm hoặc sự kiện, ví dụ: 'bei der Arbeit' (khi làm việc)."},
    {"prep": "mit", "usage": "chỉ sự đồng hành cùng ai đó", "reason": "Giới từ 'mit' đi với Dativ, chỉ sự đồng hành cùng ai đó, ví dụ: 'mit dir' (cùng với bạn)."},
    {"prep": "mit", "usage": "chỉ phương tiện hoặc công cụ", "reason": "Giới từ 'mit' đi với Dativ, chỉ phương tiện hoặc công cụ, ví dụ: 'mit dem Bus' (bằng xe buýt)."},
    {"prep": "nach", "usage": "chỉ đích đến là nơi chốn", "reason": "Giới từ 'nach' đi với Dativ, chỉ đích đến là một địa điểm, ví dụ: 'nach Berlin' (đến Berlin)."},
    {"prep": "nach", "usage": "chỉ thời gian sau một thời điểm", "reason": "Giới từ 'nach' đi với Dativ, chỉ thời gian sau một thời điểm, ví dụ: 'nach dem Unterricht' (sau giờ học)."},
    {"prep": "seit", "usage": "chỉ thời điểm bắt đầu trong quá khứ", "reason": "Giới từ 'seit' đi với Dativ, chỉ thời điểm bắt đầu trong quá khứ, ví dụ: 'seit 2010' (từ năm 2010)."},
    {"prep": "von", "usage": "chỉ sự sở hữu", "reason": "Giới từ 'von' đi với Dativ, chỉ sự sở hữu, ví dụ: 'von meiner Mutter' (của mẹ tôi)."},
    {"prep": "von", "usage": "chỉ nguồn gốc hoặc xuất xứ", "reason": "Giới từ 'von' đi với Dativ, chỉ nguồn gốc hoặc xuất xứ, ví dụ: 'von der Schule' (từ trường học)."},
    {"prep": "von", "usage": "chỉ thời gian từ một thời điểm", "reason": "Giới từ 'von' đi với Dativ, chỉ thời gian từ một thời điểm, ví dụ: 'von Montag' (từ thứ Hai)."},
    {"prep": "zu", "usage": "chỉ hướng đến một người", "reason": "Giới từ 'zu' đi với Dativ, chỉ hướng đến một người, ví dụ: 'zu meinem Freund' (đến chỗ bạn trai tôi)."},
    {"prep": "zu", "usage": "chỉ hướng đến một nơi hoặc sự kiện", "reason": "Giới từ 'zu' đi với Dativ, chỉ hướng đến một nơi hoặc sự kiện, ví dụ: 'zu der Party' (đến bữa tiệc)."},
    {"prep": "außer", "usage": "chỉ sự ngoại trừ", "reason": "Giới từ 'außer' đi với Dativ, chỉ sự ngoại trừ, ví dụ: 'außer ihm' (ngoài anh ta)."},
    {"prep": "gegenüber", "usage": "chỉ vị trí đối diện", "reason": "Giới từ 'gegenüber' đi với Dativ, chỉ vị trí đối diện, ví dụ: 'gegenüber dem Haus' (đối diện ngôi nhà)."}
]

genitiv_prepositions = [
    {"prep": "während", "usage": "chỉ thời gian diễn ra sự việc", "reason": "Giới từ 'während' đi với Genitiv, chỉ thời gian diễn ra sự việc, ví dụ: 'während des Unterrichts' (trong giờ học)."},
    {"prep": "trotz", "usage": "chỉ sự trái ngược với điều kiện", "reason": "Giới từ 'trotz' đi với Genitiv, chỉ sự trái ngược với điều kiện, ví dụ: 'trotz des Regens' (mặc dù trời mưa)."},
    {"prep": "wegen", "usage": "chỉ lý do của sự việc", "reason": "Giới từ 'wegen' đi với Genitiv, chỉ lý do của sự việc, ví dụ: 'wegen des Unfalls' (vì tai nạn)."},
    {"prep": "anstatt", "usage": "chỉ sự thay thế", "reason": "Giới từ 'anstatt' đi với Genitiv, chỉ sự thay thế, ví dụ: 'anstatt des Autos' (thay vì ô tô)."},
    {"prep": "innerhalb", "usage": "chỉ phạm vi thời gian", "reason": "Giới từ 'innerhalb' đi với Genitiv, chỉ phạm vi thời gian, ví dụ: 'innerhalb einer Woche' (trong một tuần)."},
    {"prep": "innerhalb", "usage": "chỉ phạm vi không gian", "reason": "Giới từ 'innerhalb' đi với Genitiv, chỉ phạm vi không gian, ví dụ: 'innerhalb des Hauses' (bên trong ngôi nhà)."},
    {"prep": "außerhalb", "usage": "chỉ vị trí bên ngoài", "reason": "Giới từ 'außerhalb' đi với Genitiv, chỉ vị trí bên ngoài, ví dụ: 'außerhalb der Stadt' (bên ngoài thành phố)."}
]

wechsel_prepositions = [
    {"prep": "an", "usage_akk": "chuyển động: treo hoặc đặt sát một bề mặt", "usage_dat": "vị trí: đã ở sát một bề mặt", 
     "reason_akk": "Giới từ 'an' đi với Akkusativ khi có chuyển động, chỉ hành động treo hoặc đặt sát một bề mặt, ví dụ: 'an die Wand' (lên tường).", 
     "reason_dat": "Giới từ 'an' đi với Dativ khi chỉ vị trí, đã ở sát một bề mặt, ví dụ: 'an der Wand' (trên tường)."},
    {"prep": "auf", "usage_akk": "chuyển động: đặt lên một mặt phẳng", "usage_dat": "vị trí: đã nằm trên mặt phẳng", 
     "reason_akk": "Giới từ 'auf' đi với Akkusativ khi có chuyển động, chỉ hành động đặt lên một mặt phẳng, ví dụ: 'auf den Tisch' (lên bàn).", 
     "reason_dat": "Giới từ 'auf' đi với Dativ khi chỉ vị trí, đã nằm trên một mặt phẳng, ví dụ: 'auf dem Tisch' (trên bàn)."},
    {"prep": "hinter", "usage_akk": "chuyển động: di chuyển ra phía sau", "usage_dat": "vị trí: đã ở phía sau", 
     "reason_akk": "Giới từ 'hinter' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển ra phía sau, ví dụ: 'hinter das Haus' (ra sau ngôi nhà).", 
     "reason_dat": "Giới từ 'hinter' đi với Dativ khi chỉ vị trí, đã ở phía sau, ví dụ: 'hinter dem Haus' (phía sau ngôi nhà)."},
    {"prep": "in", "usage_akk": "chuyển động: đi vào bên trong", "usage_dat": "vị trí: đã ở bên trong", 
     "reason_akk": "Giới từ 'in' đi với Akkusativ khi có chuyển động, chỉ hành động đi vào bên trong, ví dụ: 'in die Schule' (vào trường).", 
     "reason_dat": "Giới từ 'in' đi với Dativ khi chỉ vị trí, đã ở bên trong, ví dụ: 'in der Schule' (trong trường)."},
    {"prep": "neben", "usage_akk": "chuyển động: di chuyển đến bên cạnh", "usage_dat": "vị trí: đã ở bên cạnh", 
     "reason_akk": "Giới từ 'neben' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển đến bên cạnh, ví dụ: 'neben den Tisch' (đến bên cái bàn).", 
     "reason_dat": "Giới từ 'neben' đi với Dativ khi chỉ vị trí, đã ở bên cạnh, ví dụ: 'neben dem Tisch' (bên cạnh cái bàn)."},
    {"prep": "über", "usage_akk": "chuyển động: di chuyển qua phía trên", "usage_dat": "vị trí: đã ở phía trên", 
     "reason_akk": "Giới từ 'über' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển qua phía trên, ví dụ: 'über das Dach' (qua mái nhà).", 
     "reason_dat": "Giới từ 'über' đi với Dativ khi chỉ vị trí, đã ở phía trên, ví dụ: 'über dem Tisch' (phía trên cái bàn)."},
    {"prep": "unter", "usage_akk": "chuyển động: di chuyển xuống dưới", "usage_dat": "vị trí: đã ở dưới", 
     "reason_akk": "Giới từ 'unter' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển xuống dưới, ví dụ: 'unter den Tisch' (xuống dưới bàn).", 
     "reason_dat": "Giới từ 'unter' đi với Dativ khi chỉ vị trí, đã ở dưới, ví dụ: 'unter dem Tisch' (dưới cái bàn)."},
    {"prep": "vor", "usage_akk": "chuyển động: di chuyển ra phía trước", "usage_dat": "vị trí: đã ở phía trước", 
     "reason_akk": "Giới từ 'vor' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển ra phía trước, ví dụ: 'vor das Haus' (ra trước nhà).", 
     "reason_dat": "Giới từ 'vor' đi với Dativ khi chỉ vị trí, đã ở phía trước, ví dụ: 'vor dem Haus' (phía trước ngôi nhà)."},
    {"prep": "zwischen", "usage_akk": "chuyển động: di chuyển vào giữa", "usage_dat": "vị trí: đã ở giữa", 
     "reason_akk": "Giới từ 'zwischen' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển vào giữa, ví dụ: 'zwischen die Stühle' (vào giữa các ghế).", 
     "reason_dat": "Giới từ 'zwischen' đi với Dativ khi chỉ vị trí, đã ở giữa, ví dụ: 'zwischen den Stühlen' (ở giữa các ghế)."}
]

# Thiết lập cơ sở dữ liệu SQLite
def init_db():
    conn = sqlite3.connect('wrong_prepositions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wrong_prepositions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  preposition TEXT,
                  usage TEXT,
                  user_answer TEXT,
                  reason TEXT,
                  timestamp DATETIME,
                  UNIQUE(preposition, usage))''')
    conn.commit()
    conn.close()

# Hàm lưu câu trả lời sai vào database
def save_wrong_answer(preposition, usage, user_answer, reason):
    conn = sqlite3.connect('wrong_prepositions.db')
    c = conn.cursor()
    try:
        c.execute('''INSERT OR REPLACE INTO wrong_prepositions (preposition, usage, user_answer, reason, timestamp)
                     VALUES (?, ?, ?, ?, ?)''',
                     (preposition, usage, user_answer, reason, datetime.now()))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Lỗi khi lưu câu trả lời sai: {e}")
    finally:
        conn.close()

# Hàm xóa câu trả lời đúng khỏi database
def remove_correct_answer(preposition, usage):
    conn = sqlite3.connect('wrong_prepositions.db')
    c = conn.cursor()
    try:
        c.execute('''DELETE FROM wrong_prepositions WHERE preposition = ? AND usage = ?''',
                     (preposition, usage))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Lỗi khi xóa câu trả lời đúng: {e}")
    finally:
        conn.close()

# Hàm lấy câu trả lời sai cần ôn tập và đếm số câu hỏi ôn tập
def get_review_questions():
    conn = sqlite3.connect('wrong_prepositions.db')
    c = conn.cursor()
    review_time = datetime.now() - timedelta(days=1)  # Ôn tập sau 1 ngày
    c.execute('''SELECT preposition, usage, reason FROM wrong_prepositions
                 WHERE timestamp <= ?''', (review_time,))
    questions = c.fetchall()
    conn.close()
    return questions

# Hàm thử gọi API với key ngẫu nhiên
def try_with_different_key(prompt, max_attempts=MAX_ATTEMPTS, max_retries_per_key=MAX_RETRIES_PER_KEY):
    attempts = 0
    used_keys = set()

    while attempts < max_attempts:
        available_keys = [key for key in API_KEYS if key not in used_keys]
        if not available_keys:
            logger.error("Hết API key khả dụng")
            raise ResourceExhausted("Tất cả API key đều bị giới hạn tỷ lệ")

        selected_key = random.choice(available_keys)
        logger.info(f"Thử API key: {selected_key[:5]}...")
        genai.configure(api_key=selected_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        for retry in range(max_retries_per_key):
            try:
                response = model.generate_content(prompt)
                if not hasattr(response, 'text'):
                    logger.error("Phản hồi Gemini không có thuộc tính text")
                    raise ValueError("Phản hồi Gemini không hợp lệ")
                return response.text.strip()
            except ResourceExhausted as e:
                logger.warning(f"API key {selected_key[:5]}... bị giới hạn tỷ lệ (429), thử lại lần {retry + 1}/{max_retries_per_key}")
                wait_time = (2 ** retry) + random.uniform(0, 0.1)
                time.sleep(wait_time)
                if retry == max_retries_per_key - 1:
                    logger.warning(f"API key {selected_key[:5]}... hết lượt thử lại")
                    used_keys.add(selected_key)
                    attempts += 1
            except Exception as e:
                logger.error(f"Lỗi khác khi gọi Gemini API: {str(e)}")
                raise

    logger.error("Tất cả API key đều bị giới hạn tỷ lệ")
    raise ResourceExhausted("Tất cả API key đều bị giới hạn tỷ lệ")

# Hàm sửa JSON sai cú pháp
def fix_json(json_str):
    # Ghi lại chuỗi JSON gốc để debug
    logger.debug(f"Chuỗi JSON gốc: {json_str}")

    # Loại bỏ các ký tự không cần thiết
    json_str = json_str.strip()
    json_str = re.sub(r'```json\s*|\s*```', '', json_str)
    
    # Tìm cặp ngoặc {} hợp lệ
    start_idx = json_str.find('{')
    end_idx = json_str.rfind('}')
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = json_str[start_idx:end_idx + 1]
    else:
        logger.warning("Không tìm thấy cặp {} hợp lệ trong JSON")
        return None
    
    # Thử phân tích JSON
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON gốc không hợp lệ: {e}. Thử sửa...")
    
    # Sửa các lỗi JSON phổ biến
    # 1. Sửa dấu phẩy thừa trước dấu }
    json_str = re.sub(r',\s*}', '}', json_str)
    # 2. Thêm dấu nháy kép cho key nếu thiếu
    json_str = re.sub(r'(\w+)(?=\s*:)', r'"\1"', json_str)
    # 3. Thay thế nháy đơn bằng nháy kép
    json_str = json_str.replace("'", '"')
    # 4. Loại bỏ các ký tự không hợp lệ
    json_str = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', json_str)
    
    # Thử lại lần nữa
    try:
        parsed_json = json.loads(json_str)
        logger.debug(f"Chuỗi JSON sau khi sửa: {json_str}")
        return parsed_json
    except json.JSONDecodeError as e:
        logger.error(f"Không thể sửa JSON: {e}. Chuỗi JSON: {json_str}")
        return None

# Tạo stack quy tắc và đếm số câu hỏi
def create_rule_stack():
    stack = []
    
    # Đếm số quy tắc
    akk_count = len(akkusativ_prepositions)
    dat_count = len(dativ_prepositions)
    gen_count = len(genitiv_prepositions)
    wechsel_count = len(wechsel_prepositions) * 2  # Mỗi wechsel có 2 cách dùng (Akkusativ và Dativ)
    
    # Tổng số câu hỏi mới
    total_new_questions = akk_count + dat_count + gen_count + wechsel_count
    
    # Akkusativ rules
    for idx, rule in enumerate(akkusativ_prepositions):
        stack.append(f"akk_{idx}")
    
    # Dativ rules
    for idx, rule in enumerate(dativ_prepositions):
        stack.append(f"dat_{idx}")
    
    # Genitiv rules
    for idx, rule in enumerate(genitiv_prepositions):
        stack.append(f"gen_{idx}")
    
    # Wechsel rules (Akkusativ và Dativ)
    for idx, rule in enumerate(wechsel_prepositions):
        stack.append(f"wechsel_akk_{idx}")
        stack.append(f"wechsel_dat_{idx}")
    
    random.shuffle(stack)
    return stack, total_new_questions

# Hàm lấy câu ví dụ từ Gemini
def get_sentence_from_rule(rule_id):
    parts = rule_id.split('_')
    rule_type = parts[0]
    if rule_type == "wechsel":
        usage_type = parts[1]  # "akk" hoặc "dat"
        idx = int(parts[2])
        prep_data = wechsel_prepositions[idx]
        preposition = prep_data["prep"]
        usage = prep_data[f"usage_{usage_type}"]
        reason = prep_data[f"reason_{usage_type}"]
    else:
        idx = int(parts[1])
        if rule_type == "akk":
            prep_data = akkusativ_prepositions[idx]
        elif rule_type == "dat":
            prep_data = dativ_prepositions[idx]
        else:  # gen
            prep_data = genitiv_prepositions[idx]
        preposition = prep_data["prep"]
        usage = prep_data["usage"]
        reason = prep_data["reason"]
    
    # Prompt cải tiến để yêu cầu câu ví dụ và giải thích chi tiết
    prompt = (
        f"Tạo một câu ví dụ đơn giản ở trình độ A1-B1 tiếng Đức sử dụng giới từ '{preposition}' với cách dùng: '{usage}'. "
        f"Câu phải có chỗ trống để điền giới từ (dùng ___ thay cho giới từ). "
        f"Câu ví dụ cần có ngữ cảnh rõ ràng, dễ hiểu, và phù hợp với người học tiếng Đức cơ bản. "
        f"Ngoài ra, cung cấp giải thích chi tiết bằng tiếng Việt về cách dùng giới từ này, bao gồm:\n"
        f"- Ngữ cảnh sử dụng của câu ví dụ (câu này thường được dùng trong tình huống nào).\n"
        f"- Tại sao giới từ này được dùng trong trường hợp này (liên quan đến cách và ngữ nghĩa).\n"
        f"- Mẹo ghi nhớ: đưa ra một cụm từ ví dụ minh họa (theo dạng 'auf dem Tisch') để người học dễ nhớ cách dùng.\n"
        f"Giải thích phải rõ ràng, dễ hiểu, và thân thiện với người học tiếng Đức ở trình độ cơ bản.\n"
        f"Trả về JSON:\n"
        f"```json\n"
        f'{{"example": "câu có chỗ trống", "full_sentence": "câu hoàn chỉnh", "translation": "dịch nghĩa sang tiếng Việt", "explanation": "giải thích chi tiết bằng tiếng Việt (bao gồm ngữ cảnh, lý do, và mẹo ghi nhớ)"}}'
        f"\n```"
    )
    
    try:
        response = try_with_different_key(prompt)
        json_data = fix_json(response)
        
        # Nếu không thể phân tích JSON, trả về giá trị mặc định
        if json_data is None:
            logger.warning(f"Không thể phân tích JSON cho quy tắc {rule_id}. Sử dụng giá trị mặc định.")
            example = f"___ (Câu mặc định cho giới từ {preposition})"
            full_sentence = f"{preposition} (Câu mặc định)"
            translation = "Không có dịch nghĩa (lỗi phân tích JSON)"
            explanation = f"Lý do mặc định: {reason}"
            return (preposition, usage, reason, example, full_sentence, translation, explanation)
        
        return (preposition, usage, reason, json_data["example"], 
                json_data["full_sentence"], json_data["translation"], json_data["explanation"])
    except ResourceExhausted:
        logger.warning(f"Hết quota API cho quy tắc {rule_id}")
        return (preposition, usage, reason, f"___ (Không có câu - API hết quota)", 
                f"{preposition} (Không có câu)", "Không có dịch nghĩa (API hết quota)", 
                "Không có giải thích (API hết quota)")
    except Exception as e:
        logger.error(f"Lỗi khi lấy câu cho quy tắc {rule_id}: {str(e)}")
        return (preposition, usage, reason, f"___ (Không có câu - lỗi API)", 
                f"{preposition} (Không có câu)", "Không có dịch nghĩa (lỗi API)", 
                "Không có giải thích (lỗi API)")

# Lớp GUI
class GermanPrepositionTrainerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Luyện tập giới từ tiếng Đức")
        self.geometry("1380x1000")
        
        init_db()  # Khởi tạo database
        self.rule_stack, self.total_new_questions = create_rule_stack()
        self.review_questions = get_review_questions()
        self.total_review_questions = len(self.review_questions)
        self.total_questions = self.total_new_questions + self.total_review_questions  # Tổng số câu hỏi
        self.total_correct = 0  # Số câu trả lời đúng
        self.total_wrong = 0    # Số câu trả lời sai
        self.current_preposition = ""
        self.current_usage = ""
        self.current_reason = ""
        self.current_example = ""
        self.current_full_sentence = ""
        self.current_translation = ""
        self.current_explanation = ""
        self.is_answered = False
        
        self.theme = {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "button_bg": "#4CAF50",
            "button_fg": "#ffffff",
            "entry_bg": "#ffffff",
            "feedback_correct": "#055005",
            "feedback_wrong": "#750a1d"
        }
        
        self.main_frame = tk.Frame(self, bg=self.theme["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.label_title = tk.Label(self.main_frame, text="Luyện tập giới từ tiếng Đức", font=("Arial", 23, "bold"), bg=self.theme["bg"], fg=self.theme["fg"])
        self.label_title.pack(pady=5)
        
        # Nhãn hiển thị thống kê
        self.label_stats = tk.Label(self.main_frame, text=f"Tổng số câu hỏi: {self.total_questions} | Đúng: {self.total_correct} | Sai: {self.total_wrong}", font=("Arial", 16), bg=self.theme["bg"], fg=self.theme["fg"])
        self.label_stats.pack(pady=5)
        
        self.label_sentence = tk.Label(self.main_frame, text="Câu ví dụ: Chưa có", font=("Arial", 18, "bold"), bg=self.theme["bg"], fg=self.theme["fg"])
        self.label_sentence.pack(pady=10)
        
        self.label_prompt = tk.Label(self.main_frame, text="Nhập giới từ phù hợp:", font=("Arial", 18, "bold"), bg=self.theme["bg"], fg=self.theme["fg"])
        self.label_prompt.pack(pady=5)
        
        self.entry_answer = tk.Entry(self.main_frame, font=("Arial", 18, "bold"), width=10, bg=self.theme["entry_bg"], fg=self.theme["fg"])
        self.entry_answer.pack(pady=5)
        self.entry_answer.bind("<Return>", self.handle_enter)
        
        self.label_instruction = tk.Label(self.main_frame, text="Nhấn Enter để trả lời hoặc chuyển tiếp", font=("Arial", 16, "italic"), bg=self.theme["bg"], fg=self.theme["fg"])
        self.label_instruction.pack(pady=5)
        
        self.label_feedback = tk.Label(self.main_frame, text="", font=("Arial", 16), bg=self.theme["bg"], fg=self.theme["fg"], wraplength=1300, justify="left")
        self.label_feedback.pack(pady=10)
        
        self.button_next = tk.Button(self.main_frame, text="Câu tiếp theo", command=self.next_question, font=("Arial", 18, "bold"), bg=self.theme["button_bg"], fg=self.theme["button_fg"])
        self.button_next.pack(pady=5)
        
        self.next_question()
    
    def handle_enter(self, event):
        if not self.is_answered:
            self.check_answer()
        else:
            self.next_question()
    
    def next_question(self):
        # Kiểm tra câu ôn tập trước
        if self.review_questions:
            preposition, usage, reason = random.choice(self.review_questions)
            self.current_preposition = preposition
            self.current_usage = usage
            self.current_reason = reason
            # Tạo lại câu ví dụ và giải thích cho câu ôn tập
            prompt = (
                f"Tạo một câu ví dụ đơn giản ở trình độ A1-B1 tiếng Đức sử dụng giới từ '{preposition}' với cách dùng: '{usage}'. "
                f"Câu phải có chỗ trống để điền giới từ (dùng ___ thay cho giới từ). "
                f"Câu ví dụ cần có ngữ cảnh rõ ràng, dễ hiểu, và phù hợp với người học tiếng Đức cơ bản. "
                f"Ngoài ra, cung cấp giải thích chi tiết bằng tiếng Việt về cách dùng giới từ này, bao gồm:\n"
                f"- Ngữ cảnh sử dụng của câu ví dụ (câu này thường được dùng trong tình huống nào).\n"
                f"- Tại sao giới từ này được dùng trong trường hợp này (liên quan đến cách và ngữ nghĩa).\n"
                f"- Mẹo ghi nhớ: đưa ra một cụm từ ví dụ minh họa (theo dạng 'auf dem Tisch') để người học dễ nhớ cách dùng.\n"
                f"Giải thích phải rõ ràng, dễ hiểu, và thân thiện với người học tiếng Đức ở trình độ cơ bản.\n"
                f"Trả về JSON:\n"
                f"```json\n"
                f'{{"example": "câu có chỗ trống", "full_sentence": "câu hoàn chỉnh", "translation": "dịch nghĩa sang tiếng Việt", "explanation": "giải thích chi tiết bằng tiếng Việt (bao gồm ngữ cảnh, lý do, và mẹo ghi nhớ)"}}'
                f"\n```"
            )
            try:
                response = try_with_different_key(prompt)
                json_data = fix_json(response)
                if json_data is None:
                    self.current_example = f"___ (Câu mặc định cho giới từ {preposition})"
                    self.current_full_sentence = f"{preposition} (Câu mặc định)"
                    self.current_translation = "Không có dịch nghĩa (lỗi phân tích JSON)"
                    self.current_explanation = f"Lý do mặc định: {reason}"
                else:
                    self.current_example = json_data["example"]
                    self.current_full_sentence = json_data["full_sentence"]
                    self.current_translation = json_data["translation"]
                    self.current_explanation = json_data["explanation"]
            except:
                self.current_example = f"___ (Không có câu - lỗi API)"
                self.current_full_sentence = f"{preposition} (Không có câu)"
                self.current_translation = "Không có dịch nghĩa (lỗi API)"
                self.current_explanation = "Không có giải thích (lỗi API)"
            self.review_questions.remove((preposition, usage, reason))
        else:
            if not self.rule_stack:
                messagebox.showinfo("Hoàn thành", f"Bạn đã hoàn thành! Tổng số câu hỏi: {self.total_questions}\nĐúng: {self.total_correct}\nSai: {self.total_wrong}")
                self.entry_answer.config(state=tk.DISABLED)
                self.button_next.config(state=tk.DISABLED)
                return
            rule_id = self.rule_stack.pop(0)
            (self.current_preposition, self.current_usage, self.current_reason, self.current_example, 
             self.current_full_sentence, self.current_translation, self.current_explanation) = get_sentence_from_rule(rule_id)
        
        self.label_sentence.config(text=f"Câu ví dụ: {self.current_example}")
        self.label_feedback.config(text="", fg=self.theme["fg"])
        self.entry_answer.delete(0, tk.END)
        self.entry_answer.config(state=tk.NORMAL)
        self.is_answered = False
        self.entry_answer.focus()
    
    def check_answer(self):
        user_answer = self.entry_answer.get().strip().lower()
        if not user_answer:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập giới từ!")
            return
        
        is_correct = user_answer == self.current_preposition.lower()
        feedback_text = (
            f"Câu hoàn chỉnh: '{self.current_full_sentence}' (Nghĩa: {self.current_translation})\n\n"
            f"Giải thích chi tiết:\n{self.current_explanation}"
        )
        
        if is_correct:
            self.total_correct += 1
            self.label_feedback.config(
                text=f"Đúng! 🎉\n{feedback_text}",
                fg=self.theme["feedback_correct"]
            )
            remove_correct_answer(self.current_preposition, self.current_usage)
        else:
            self.total_wrong += 1
            self.label_feedback.config(
                text=f"Sai! 😔 Đáp án đúng là '{self.current_preposition}'.\n{feedback_text}",
                fg=self.theme["feedback_wrong"]
            )
            save_wrong_answer(self.current_preposition, self.current_usage, user_answer, self.current_reason)
        
        # Cập nhật thống kê
        self.label_stats.config(text=f"Tổng số câu hỏi: {self.total_questions} | Đúng: {self.total_correct} | Sai: {self.total_wrong}")
        
        self.is_answered = True
        self.entry_answer.config(state=tk.NORMAL)
        self.entry_answer.focus()

if __name__ == "__main__":
    app = GermanPrepositionTrainerGUI()
    app.mainloop()