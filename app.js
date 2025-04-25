// API keys từ config.json (cần thay bằng khóa hợp lệ)
const API_KEYS = [
    "AIzaSyCdxcJf9F3myEQjI_1ogbS-6_0RLRtOEY8",
    "AIzaSyCp_VB-bpgQ6wEvVZBR04akkXcSVvwtoiQ",
    "AIzaSyAXlZH48sepbUXX5yV7IsnYmdMiwynWyBc",
    "AIzaSyCTRvEKv14mwiKzG6-6cZ_o0WI3BHBl3ZI",
    "AIzaSyDB7FnEBtoGs_BNoQx6gHOVJTwGBGgGOgA",
    "AIzaSyAm8YrImdMCWZrh8Pot2HDs35y1gV1wQAU",
    "AIzaSyCG4R2bDJmU3nE13ZWeuusLDCBxfBOjzFE",
    "AIzaSyAnG2PgKsyyeWZeH6fGti-UzNHx2_hKF2c",
    // Thêm các khóa API hợp lệ từ Google Cloud Console
];

let PRIMARY_KEY = API_KEYS[Math.floor(Math.random() * API_KEYS.length)];
let VERIFY_KEY = API_KEYS.find(key => key !== PRIMARY_KEY) || API_KEYS[0];

// Dữ liệu giới từ
const akkusativPrepositions = [
    { prep: "durch", usage: "chỉ hướng xuyên qua một không gian hoặc nơi chốn", reason: "Giới từ 'durch' đi với Akkusativ, thường chỉ hướng xuyên qua một không gian hoặc nơi chốn, ví dụ: 'durch den Park' (qua công viên)." },
    { prep: "durch", usage: "chỉ sự thông qua một phương tiện hoặc cách thức", reason: "Giới từ 'durch' đi với Akkusativ, chỉ sự thông qua một phương tiện hoặc cách thức, ví dụ: 'durch das Telefon' (qua điện thoại)." },
    { prep: "für", usage: "dành cho ai đó", reason: "Giới từ 'für' đi với Akkusativ, mang ý nghĩa dành cho một người, ví dụ: 'für dich' (cho bạn)." },
    { prep: "für", usage: "mục đích", reason: "Giới từ 'für' đi với Akkusativ, chỉ mục đích của hành động, ví dụ: 'für die Reise' (cho chuyến đi)." },
    { prep: "für", usage: "thời gian", reason: "Giới từ 'für' đi với Akkusativ, chỉ khoảng thời gian cụ thể, ví dụ: 'für eine Woche' (trong một tuần)." },
    { prep: "gegen", usage: "chỉ sự đối kháng hoặc chống lại", reason: "Giới từ 'gegen' đi với Akkusativ, chỉ sự đối kháng hoặc chống lại, ví dụ: 'gegen den Wind' (chống lại cơn gió)." },
    { prep: "gegen", usage: "chỉ hướng đến về thời gian hoặc không gian", reason: "Giới từ 'gegen' đi với Akkusativ, chỉ hướng đến về thời gian hoặc không gian, ví dụ: 'gegen Abend' (vào buổi tối)." },
    { prep: "ohne", usage: "chỉ sự thiếu vắng", reason: "Giới từ 'ohne' đi với Akkusativ, chỉ sự thiếu vắng ai đó hoặc cái gì đó, ví dụ: 'ohne mein Gepäck' (không có hành lý)." },
    { prep: "um", usage: "chỉ vị trí xung quanh một vật", reason: "Giới từ 'um' đi với Akkusativ, chỉ vị trí xung quanh một vật, ví dụ: 'um den Tisch' (quanh cái bàn)." },
    { prep: "um", usage: "chỉ thời gian cụ thể", reason: "Giới từ 'um' đi với Akkusativ, chỉ thời gian cụ thể, ví dụ: 'um drei Uhr' (lúc 3 giờ)." },
    { prep: "um", usage: "chỉ sự thay đổi hoặc chuyển đổi", reason: "Giới từ 'um' đi với Akkusativ, chỉ sự thay đổi hoặc chuyển đổi, ví dụ: 'um ein Ticket' (để đổi lấy vé)." }
];

const dativPrepositions = [
    { prep: "aus", usage: "chỉ nguồn gốc hoặc xuất xứ", reason: "Giới từ 'aus' đi với Dativ, chỉ nguồn gốc hoặc xuất xứ, ví dụ: 'aus Deutschland' (từ Đức)." },
    { prep: "aus", usage: "chỉ hành động ra khỏi một nơi", reason: "Giới từ 'aus' đi với Dativ, chỉ hành động ra khỏi một nơi, ví dụ: 'aus dem Haus' (ra khỏi nhà)." },
    { prep: "bei", usage: "chỉ vị trí gần một người", reason: "Giới từ 'bei' đi với Dativ, chỉ vị trí gần một người, ví dụ: 'bei meiner Freundin' (ở chỗ bạn gái tôi)." },
    { prep: "bei", usage: "chỉ thời điểm hoặc sự kiện", reason: "Giới từ 'bei' đi với Dativ, chỉ thời điểm hoặc sự kiện, ví dụ: 'bei der Arbeit' (khi làm việc)." },
    { prep: "mit", usage: "chỉ sự đồng hành cùng ai đó", reason: "Giới từ 'mit' đi với Dativ, chỉ sự đồng hành cùng ai đó, ví dụ: 'mit dir' (cùng với bạn)." },
    { prep: "mit", usage: "chỉ phương tiện hoặc công cụ", reason: "Giới từ 'mit' đi với Dativ, chỉ phương tiện hoặc công cụ, ví dụ: 'mit dem Bus' (bằng xe buýt)." },
    { prep: "nach", usage: "chỉ đích đến là nơi chốn", reason: "Giới từ 'nach' đi với Dativ, chỉ đích đến là một địa điểm, ví dụ: 'nach Berlin' (đến Berlin)." },
    { prep: "nach", usage: "chỉ thời gian sau một thời điểm", reason: "Giới từ 'nach' đi với Dativ, chỉ thời gian sau một thời điểm, ví dụ: 'nach dem Unterricht' (sau giờ học)." },
    { prep: "seit", usage: "chỉ thời điểm bắt đầu trong quá khứ", reason: "Giới từ 'seit' đi với Dativ, chỉ thời điểm bắt đầu trong quá khứ, ví dụ: 'seit 2010' (từ năm 2010)." },
    { prep: "von", usage: "chỉ sự sở hữu", reason: "Giới từ 'von' đi với Dativ, chỉ sự sở hữu, ví dụ: 'von meiner Mutter' (của mẹ tôi)." },
    { prep: "von", usage: "chỉ nguồn gốc hoặc xuất xứ", reason: "Giới từ 'von' đi với Dativ, chỉ nguồn gốc hoặc xuất xứ, ví dụ: 'von der Schule' (từ trường học)." },
    { prep: "von", usage: "chỉ thời gian từ một thời điểm", reason: "Giới từ 'von' đi với Dativ, chỉ thời gian từ một thời điểm, ví dụ: 'von Montag' (từ thứ Hai)." },
    { prep: "zu", usage: "chỉ hướng đến một người", reason: "Giới từ 'zu' đi với Dativ, chỉ hướng đến một người, ví dụ: 'zu meinem Freund' (đến chỗ bạn trai tôi)." },
    { prep: "zu", usage: "chỉ hướng đến một nơi hoặc sự kiện", reason: "Giới từ 'zu' đi với Dativ, chỉ hướng đến một nơi hoặc sự kiện, ví dụ: 'zu der Party' (đến bữa tiệc)." },
    { prep: "außer", usage: "chỉ sự ngoại trừ", reason: "Giới từ 'außer' đi với Dativ, chỉ sự ngoại trừ, ví dụ: 'außer ihm' (ngoài anh ta)." },
    { prep: "gegenüber", usage: "chỉ vị trí đối diện", reason: "Giới từ 'gegenüber' đi với Dativ, chỉ vị trí đối diện, ví dụ: 'gegenüber dem Haus' (đối diện ngôi nhà)." }
];

const genitivPrepositions = [
    { prep: "während", usage: "chỉ thời gian diễn ra sự việc", reason: "Giới từ 'während' đi với Genitiv, chỉ thời gian diễn ra sự việc, ví dụ: 'während des Unterrichts' (trong giờ học)." },
    { prep: "trotz", usage: "chỉ sự trái ngược với điều kiện", reason: "Giới từ 'trotz' đi với Genitiv, chỉ sự trái ngược với điều kiện, ví dụ: 'trotz des Regens' (mặc dù trời mưa)." },
    { prep: "wegen", usage: "chỉ lý do của sự việc", reason: "Giới từ 'wegen' đi với Genitiv, chỉ lý do của sự việc, ví dụ: 'wegen des Unfalls' (vì tai nạn)." },
    { prep: "anstatt", usage: "chỉ sự thay thế", reason: "Giới từ 'anstatt' đi với Genitiv, chỉ sự thay thế, ví dụ: 'anstatt des Autos' (thay vì ô tô)." },
    { prep: "innerhalb", usage: "chỉ phạm vi thời gian", reason: "Giới từ 'innerhalb' đi với Genitiv, chỉ phạm vi thời gian, ví dụ: 'innerhalb einer Woche' (trong một tuần)." },
    { prep: "innerhalb", usage: "chỉ phạm vi không gian", reason: "Giới từ 'innerhalb' đi với Genitiv, chỉ phạm vi không gian, ví dụ: 'innerhalb des Hauses' (bên trong ngôi nhà)." },
    { prep: "außerhalb", usage: "chỉ vị trí bên ngoài", reason: "Giới từ 'außerhalb' đi với Genitiv, chỉ vị trí bên ngoài, ví dụ: 'außerhalb der Stadt' (bên ngoài thành phố)." }
];

const wechselPrepositions = [
    { prep: "an", usage_akk: "chuyển động: treo hoặc đặt sát một bề mặt", usage_dat: "vị trí: đã ở sát một bề mặt", 
      reason_akk: "Giới từ 'an' đi với Akkusativ khi có chuyển động, chỉ hành động treo hoặc đặt sát một bề mặt, ví dụ: 'an die Wand' (lên tường).", 
      reason_dat: "Giới từ 'an' đi với Dativ khi chỉ vị trí, đã ở sát một bề mặt, ví dụ: 'an der Wand' (trên tường)." },
    { prep: "auf", usage_akk: "chuyển động: đặt lên một mặt phẳng", usage_dat: "vị trí: đã nằm trên mặt phẳng", 
      reason_akk: "Giới từ 'auf' đi với Akkusativ khi có chuyển động, chỉ hành động đặt lên một mặt phẳng, ví dụ: 'auf den Tisch' (lên bàn).", 
      reason_dat: "Giới từ 'auf' đi với Dativ khi chỉ vị trí, đã nằm trên một mặt phẳng, ví dụ: 'auf dem Tisch' (trên bàn)." },
    { prep: "hinter", usage_akk: "chuyển động: di chuyển ra phía sau", usage_dat: "vị trí: đã ở phía sau", 
      reason_akk: "Giới từ 'hinter' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển ra phía sau, ví dụ: 'hinter das Haus' (ra sau ngôi nhà).", 
      reason_dat: "Giới từ 'hinter' đi với Dativ khi chỉ vị trí, đã ở phía sau, ví dụ: 'hinter dem Haus' (phía sau ngôi nhà)." },
    { prep: "in", usage_akk: "chuyển động: đi vào bên trong", usage_dat: "vị trí: đã ở bên trong", 
      reason_akk: "Giới từ 'in' đi với Akkusativ khi có chuyển động, chỉ hành động đi vào bên trong, ví dụ: 'in die Schule' (vào trường).", 
      reason_dat: "Giới từ 'in' đi với Dativ khi chỉ vị trí, đã ở bên trong, ví dụ: 'in der Schule' (trong trường)." },
    { prep: "neben", usage_akk: "chuyển động: di chuyển đến bên cạnh", usage_dat: "vị trí: đã ở bên cạnh", 
      reason_akk: "Giới từ 'neben' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển đến bên cạnh, ví dụ: 'neben den Tisch' (đến bên cái bàn).", 
      reason_dat: "Giới từ 'neben' đi với Dativ khi chỉ vị trí, đã ở bên cạnh, ví dụ: 'neben dem Tisch' (bên cạnh cái bàn)." },
    { prep: "über", usage_akk: "chuyển động: di chuyển qua phía trên", usage_dat: "vị trí: đã ở phía trên", 
      reason_akk: "Giới từ 'über' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển qua phía trên, ví dụ: 'über das Dach' (qua mái nhà).", 
      reason_dat: "Giới từ 'über' đi với Dativ khi chỉ vị trí, đã ở phía trên, ví dụ: 'über dem Tisch' (phía trên cái bàn)." },
    { prep: "unter", usage_akk: "chuyển động: di chuyển xuống dưới", usage_dat: "vị trí: đã ở dưới", 
      reason_akk: "Giới từ 'unter' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển xuống dưới, ví dụ: 'unter den Tisch' (xuống dưới bàn).", 
      reason_dat: "Giới từ 'unter' đi với Dativ khi chỉ vị trí, đã ở dưới, ví dụ: 'unter dem Tisch' (dưới cái bàn)." },
    { prep: "vor", usage_akk: "chuyển động: di chuyển ra phía trước", usage_dat: "vị trí: đã ở phía trước", 
      reason_akk: "Giới từ 'vor' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển ra phía trước, ví dụ: 'vor das Haus' (ra trước nhà).", 
      reason_dat: "Giới từ 'vor' đi với Dativ khi chỉ vị trí, đã ở phía trước, ví dụ: 'vor dem Haus' (phía trước ngôi nhà)." },
    { prep: "zwischen", usage_akk: "chuyển động: di chuyển vào giữa", usage_dat: "vị trí: đã ở giữa", 
      reason_akk: "Giới từ 'zwischen' đi với Akkusativ khi có chuyển động, chỉ hành động di chuyển vào giữa, ví dụ: 'zwischen die Stühle' (vào giữa các ghế).", 
      reason_dat: "Giới từ 'zwischen' đi với Dativ khi chỉ vị trí, đã ở giữa, ví dụ: 'zwischen den Stühlen' (ở giữa các ghế)." }
];

// Biến trạng thái
let ruleStack = [];
let totalNewQuestions = 0;
let totalReviewQuestions = 0;
let totalQuestions = 0;
let totalCorrect = 0;
let totalWrong = 0;
let currentPreposition = "";
let currentUsage = "";
let currentReason = "";
let currentExample = "";
let currentFullSentence = "";
let currentTranslation = "";
let currentExplanation = "";
let isAnswered = false;
let reviewQuestions = JSON.parse(localStorage.getItem('wrongPrepositions') || '[]');
let lastWrongQuestion = null; // Lưu câu sai cuối cùng để tránh lặp lại
const MAX_API_RETRIES = 3;

// Hiển thị popup
function showPopup(title, message) {
    document.getElementById('popupTitle').textContent = title;
    document.getElementById('popupMessage').textContent = message;
    document.getElementById('popup').classList.remove('hidden');
    document.body.classList.add('no-scroll');
}

// Ẩn popup
function hidePopup() {
    document.getElementById('popup').classList.add('hidden');
    document.body.classList.remove('no-scroll');
}

// Hiển thị popup danh sách câu sai
function showWrongSentencesPopup() {
    const wrongSentencesList = document.getElementById('wrongSentencesList');
    if (reviewQuestions.length === 0) {
        wrongSentencesList.innerHTML = '<p class="text-center">Chưa có câu nào sai!</p>';
    } else {
        wrongSentencesList.innerHTML = '<ul>' + reviewQuestions.map((item, index) => `
            <li class="wrong-item">
                <p><strong>${index + 1}. Câu:</strong> ${item.example} <button class="speak-wrong-btn" onclick="speakSentence('${item.fullSentence.replace(/'/g, "\\'")}')">Nghe</button></p>
                <p><strong>Giới từ đúng:</strong> ${item.preposition}</p>
                <p><strong>Giới từ bạn nhập:</strong> ${item.userAnswer}</p>
                <p><strong>Lý do:</strong> ${item.reason}</p>
                <p><strong>Giải thích:</strong> ${item.explanation}</p>
            </li>
        `).join('') + '</ul>';
    }
    document.getElementById('wrongSentencesPopup').classList.remove('hidden');
    document.body.classList.add('no-scroll');
}

// Ẩn popup danh sách câu sai
function hideWrongSentencesPopup() {
    document.getElementById('wrongSentencesPopup').classList.add('hidden');
    document.body.classList.remove('no-scroll');
}

// Gọi API Gemini
async function callGeminiAPI(prompt, apiKey) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent?key=${apiKey}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        return fixJson(data.candidates[0].content.parts[0].text);
    } catch (error) {
        throw error;
    }
}

// Thử với các khóa API khác nhau
async function tryWithDifferentKey(prompt, excludedKey) {
    const availableKeys = API_KEYS.filter(key => key !== excludedKey);
    for (const key of availableKeys) {
        try {
            const response = await callGeminiAPI(prompt, key);
            if (response) {
                PRIMARY_KEY = key;
                return response;
            }
        } catch (error) {
            if (error.message.includes('429')) {
                await new Promise(resolve => setTimeout(resolve, 500));
                continue;
            }
            console.warn(`Lỗi với key ${key.slice(0, 5)}...: ${error}`);
        }
    }
    throw new Error('Tất cả API key không hoạt động');
}

// Sửa JSON không hợp lệ
function fixJson(jsonStr) {
    jsonStr = jsonStr.replace(/```json\s*|\s*```/g, '').trim();
    const startIdx = jsonStr.indexOf('{');
    const endIdx = jsonStr.lastIndexOf('}');
    if (startIdx !== -1 && endIdx !== -1 && endIdx > startIdx) {
        jsonStr = jsonStr.slice(startIdx, endIdx + 1);
    } else {
        return null;
    }

    try {
        return JSON.parse(jsonStr);
    } catch (e) {
        jsonStr = jsonStr.replace(/,\s*}/g, '}').replace(/(\w+)(?=\s*:)/g, '"$1"');
        try {
            return JSON.parse(jsonStr);
        } catch {
            return null;
        }
    }
}

// Tạo stack quy tắc
function createRuleStack() {
    const stack = [];
    totalNewQuestions = akkusativPrepositions.length + dativPrepositions.length + genitivPrepositions.length + (wechselPrepositions.length * 2);

    akkusativPrepositions.forEach((_, idx) => stack.push(`akk_${idx}`));
    dativPrepositions.forEach((_, idx) => stack.push(`dat_${idx}`));
    genitivPrepositions.forEach((_, idx) => stack.push(`gen_${idx}`));
    wechselPrepositions.forEach((_, idx) => {
        stack.push(`wechsel_akk_${idx}`);
        stack.push(`wechsel_dat_${idx}`);
    });

    // Xáo trộn stack
    for (let i = stack.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [stack[i], stack[j]] = [stack[j], stack[i]];
    }

    console.log('ruleStack created:', stack);
    return stack;
}

// Tạo câu ví dụ từ quy tắc
async function getSentenceFromRule(ruleId) {
    console.log('getSentenceFromRule called, ruleId:', ruleId);
    const parts = ruleId.split('_');
    const ruleType = parts[0];
    let prepData, preposition, usage, reason;

    if (ruleType === 'wechsel') {
        const usageType = parts[1];
        const idx = parseInt(parts[2]);
        prepData = wechselPrepositions[idx];
        preposition = prepData.prep;
        usage = prepData[`usage_${usageType}`];
        reason = prepData[`reason_${usageType}`];
    } else {
        const idx = parseInt(parts[1]);
        prepData = ruleType === 'akk' ? akkusativPrepositions[idx] :
                  ruleType === 'dat' ? dativPrepositions[idx] : genitivPrepositions[idx];
        preposition = prepData.prep;
        usage = prepData.usage;
        reason = prepData.reason;
    }

    const prompt = `
Tạo một câu ví dụ đơn giản ở trình độ A1-B1 tiếng Đức sử dụng giới từ '${preposition}' với cách dùng: '${usage}'.
Câu phải có chỗ trống để điền giới từ (dùng ___ thay cho giới từ).
Câu ví dụ cần có ngữ cảnh rõ ràng, dễ hiểu, và phù hợp với người học tiếng Đức cơ bản.
Sử dụng ngữ cảnh ngẫu nhiên khác nhau mỗi lần (seed: ${Math.random()}).
Ngoài ra, cung cấp giải thích chi tiết bằng tiếng Việt về cách dùng giới từ này, bao gồm:
- Ngữ cảnh sử dụng của câu ví dụ (câu này thường được dùng trong tình huống nào).
- Tại sao giới từ này được dùng trong trường hợp này (liên quan đến cách và ngữ nghĩa).
- Mẹo ghi nhớ: đưa ra một cụm từ ví dụ minh họa (theo dạng 'auf dem Tisch') để người học dễ nhớ cách dùng.
Giải thích phải rõ ràng, dễ hiểu, và thân thiện với người học tiếng Đức ở trình độ cơ bản.
Trả về JSON:
{
  "example": "câu có chỗ trống",
  "full_sentence": "câu hoàn chỉnh",
  "translation": "dịch nghĩa sang tiếng Việt",
  "explanation": "giải thích chi tiết bằng tiếng Việt (bao gồm ngữ cảnh, lý do, và mẹo ghi nhớ)"
}
`;

    for (let retry = 0; retry < MAX_API_RETRIES; retry++) {
        try {
            const response = await tryWithDifferentKey(prompt, VERIFY_KEY);
            if (!response) continue;

            console.log('getSentenceFromRule response:', response);
            return [
                preposition,
                usage,
                reason,
                response.example,
                response.full_sentence,
                response.translation,
                response.explanation
            ];
        } catch (error) {
            console.warn(`Lỗi API retry ${retry + 1}: ${error}`);
            if (retry === MAX_API_RETRIES - 1) {
                showPopup('Lỗi API', 'Không thể lấy câu mới. Vui lòng kiểm tra kết nối hoặc thử lại sau.');
                return [
                    preposition,
                    usage,
                    reason,
                    `___ (Không có câu - lỗi API)`,
                    `${preposition} (Không có câu)`,
                    "Không có dịch nghĩa (lỗi API)",
                    "Không có giải thích (lỗi API)"
                ];
            }
            await new Promise(resolve => setTimeout(resolve, 500));
        }
    }
}

// Phát âm câu ví dụ
function speakSentence(sentence) {
    if (!('speechSynthesis' in window)) {
        showPopup('Lỗi phát âm', 'Trình duyệt không hỗ trợ Web Speech API. Vui lòng sử dụng trình duyệt hiện đại như Chrome, Edge, hoặc Safari mới nhất.');
        return;
    }

    const utterance = new SpeechSynthesisUtterance(sentence);
    utterance.lang = 'de-DE';
    utterance.rate = 0.9;

    const voices = window.speechSynthesis.getVoices();
    const germanVoice = voices.find(voice => voice.lang === 'de-DE' || voice.lang.startsWith('de'));

    if (germanVoice) {
        utterance.voice = germanVoice;
    } else {
        showPopup('Cảnh báo phát âm', 'Không tìm thấy giọng tiếng Đức trên thiết bị. Vui lòng cài đặt giọng tiếng Đức hoặc thử trình duyệt khác (Chrome/Edge).');
    }

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);

    utterance.onerror = (event) => {
        showPopup('Lỗi phát âm', `Không thể phát âm "${sentence}": ${event.error}. Vui lòng kiểm tra cài đặt âm thanh hoặc thử lại.`);
    };
}

// Đảm bảo danh sách giọng nói được tải trước
function loadVoices() {
    return new Promise((resolve) => {
        const voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
            resolve();
        } else {
            window.speechSynthesis.onvoiceschanged = () => {
                setTimeout(() => resolve(), 100);
            };
        }
    });
}

// Lưu câu trả lời sai
function saveWrongAnswer(preposition, usage, userAnswer, reason, example, fullSentence, translation, explanation) {
    reviewQuestions.push({ preposition, usage, userAnswer, reason, example, fullSentence, translation, explanation });
    localStorage.setItem('wrongPrepositions', JSON.stringify(reviewQuestions.slice(-100)));
}

// Xóa câu trả lời đúng
function removeCorrectAnswer(preposition, usage) {
    reviewQuestions = reviewQuestions.filter(q => q.preposition !== preposition || q.usage !== usage);
    localStorage.setItem('wrongPrepositions', JSON.stringify(reviewQuestions));
}

// Cập nhật thống kê
function updateStats() {
    totalQuestions = totalCorrect + totalWrong;
    document.getElementById('stats').textContent = `Tổng số câu hỏi: ${totalQuestions} | Đúng: ${totalCorrect} | Sai: ${totalWrong}`;
}

// Chuyển sang câu tiếp theo
async function nextSentence() {
    console.log('nextSentence called, isAnswered:', isAnswered, 'ruleStack length:', ruleStack.length, 'reviewQuestions length:', reviewQuestions.length);
    
    if (ruleStack.length > 0) {
        const ruleId = ruleStack.shift();
        try {
            [currentPreposition, currentUsage, currentReason, currentExample, currentFullSentence, currentTranslation, currentExplanation] = await getSentenceFromRule(ruleId);
        } catch (error) {
            console.error('Lỗi trong getSentenceFromRule:', error);
            showPopup('Lỗi', 'Không thể lấy câu mới. Vui lòng thử lại.');
            return;
        }
    } else if (reviewQuestions.length > 0) {
        const availableQuestions = reviewQuestions.filter(q => 
            !lastWrongQuestion || (q.preposition !== lastWrongQuestion.preposition || q.usage !== lastWrongQuestion.usage)
        );
        if (availableQuestions.length === 0) {
            const question = reviewQuestions[Math.floor(Math.random() * reviewQuestions.length)];
            currentPreposition = question.preposition;
            currentUsage = question.usage;
            currentReason = question.reason;
            currentExample = question.example;
            currentFullSentence = question.fullSentence;
            currentTranslation = question.translation;
            currentExplanation = question.explanation;
        } else {
            const question = availableQuestions[Math.floor(Math.random() * availableQuestions.length)];
            currentPreposition = question.preposition;
            currentUsage = question.usage;
            currentReason = question.reason;
            currentExample = question.example;
            currentFullSentence = question.fullSentence;
            currentTranslation = question.translation;
            currentExplanation = question.explanation;
            reviewQuestions = reviewQuestions.filter(q => q.preposition !== currentPreposition || q.usage !== currentUsage);
            localStorage.setItem('wrongPrepositions', JSON.stringify(reviewQuestions));
        }
    } else {
        showPopup('Hoàn thành', `Bạn đã hoàn thành!\nTổng số câu hỏi: ${totalQuestions}\nĐúng: ${totalCorrect}\nSai: ${totalWrong}`);
        document.getElementById('answer').disabled = true;
        document.getElementById('nextBtn').disabled = true;
        document.getElementById('speakBtn').disabled = true;
        document.getElementById('viewWrongBtn').disabled = true;
        document.getElementById('clearWrongBtn').disabled = true;
        return;
    }

    document.getElementById('sentence').textContent = currentExample;
    document.getElementById('sentence').innerHTML = currentExample; // Đảm bảo cập nhật giao diện
    document.getElementById('feedback').textContent = '';
    document.getElementById('feedback').classList.remove('correct', 'wrong');
    document.getElementById('answer').value = '';
    document.getElementById('answer').disabled = false;
    isAnswered = false;
    document.getElementById('answer').focus();
    console.log('nextSentence completed, new sentence:', currentExample, 'preposition:', currentPreposition);
}

// Kiểm tra câu trả lời
function checkAnswer() {
    console.log('checkAnswer called, isAnswered:', isAnswered);
    const userAnswer = document.getElementById('answer').value.trim().toLowerCase();
    if (!userAnswer) {
        showPopup('Cảnh báo', 'Vui lòng nhập giới từ!');
        return;
    }

    const isCorrect = userAnswer === currentPreposition.toLowerCase();
    const feedbackText = `Câu: ${currentFullSentence}\nNghĩa: ${currentTranslation}\nLý do: ${currentReason}`;

    if (isCorrect) {
        totalCorrect++;
        document.getElementById('feedback').textContent = `Đúng! 🎉\n${feedbackText}`;
        document.getElementById('feedback').classList.add('correct');
        removeCorrectAnswer(currentPreposition, currentUsage);
        lastWrongQuestion = null;
    } else {
        totalWrong++;
        document.getElementById('feedback').textContent = `Sai! 😔 Đáp án đúng: ${currentPreposition}\n${feedbackText}`;
        document.getElementById('feedback').classList.add('wrong');
        lastWrongQuestion = { preposition: currentPreposition, usage: currentUsage };
        saveWrongAnswer(currentPreposition, currentUsage, userAnswer, currentReason, currentExample, currentFullSentence, currentTranslation, currentExplanation);
    }

    updateStats();
    isAnswered = true;
    speakSentence(currentFullSentence);
    document.getElementById('answer').focus();
    console.log('checkAnswer completed, isCorrect:', isCorrect, 'isAnswered:', isAnswered);
}

// Sự kiện
document.getElementById('nextBtn').addEventListener('click', () => {
    console.log('nextBtn clicked, isAnswered:', isAnswered);
    if (isAnswered) {
        nextSentence();
    } else {
        showPopup('Cảnh báo', 'Vui lòng trả lời trước khi chuyển câu!');
    }
});

// Sự kiện đóng popup khi nhấn ngoài
document.getElementById('popup').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) {
        console.log('Clicked outside popup, closing');
        hidePopup();
    }
});

document.getElementById('wrongSentencesPopup').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) {
        console.log('Clicked outside wrongSentencesPopup, closing');
        hideWrongSentencesPopup();
    }
});

document.getElementById('speakBtn').addEventListener('click', () => {
    console.log('speakBtn clicked');
    speakSentence(currentFullSentence);
});

document.getElementById('viewWrongBtn').addEventListener('click', () => {
    console.log('viewWrongBtn clicked, reviewQuestions length:', reviewQuestions.length);
    showWrongSentencesPopup();
});

document.getElementById('clearWrongBtn').addEventListener('click', () => {
    console.log('clearWrongBtn clicked');
    reviewQuestions = [];
    localStorage.setItem('wrongPrepositions', '[]');
    showPopup('Thông báo', 'Đã xóa lịch sử câu sai!');
});

document.getElementById('popupClose').addEventListener('click', hidePopup);
document.getElementById('wrongSentencesPopupClose').addEventListener('click', hideWrongSentencesPopup);

document.getElementById('answer').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        console.log('Enter pressed, isAnswered:', isAnswered);
        if (!isAnswered) {
            checkAnswer();
        } else {
            nextSentence();
        }
    }
});

// Khởi tạo
async function init() {
    console.log('init started');
    await loadVoices();
    ruleStack = createRuleStack();
    totalReviewQuestions = reviewQuestions.length;
    totalQuestions = totalNewQuestions + totalReviewQuestions;
    updateStats();
    await nextSentence();
    console.log('init completed');
}

init();