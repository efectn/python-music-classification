/// 1) Tema değiştir
function toggleTheme() {
  const html = document.documentElement;
  const body = document.body;
  const icon = document.getElementById('themeIcon');
  const isDark = html.getAttribute('data-bs-theme') === 'dark';

  // Yeni tema belirle
  const nextTheme = isDark ? 'light' : 'dark';

  // Hem Bootstrap için hem de kendi CSS'iniz için attribute'u güncelle
  html.setAttribute('data-bs-theme', nextTheme);
  body.setAttribute('data-theme', nextTheme);

  // Iconu değiştir
  icon.className = isDark ? 'bi bi-moon-fill' : 'bi bi-sun-fill';

  // Lokal saklama
  localStorage.setItem('theme', nextTheme);
}

// 2) Şifre canlı doğrulama
function validatePassword() {
  const pw = document.getElementById('password')?.value || '';
  const rules = {
    length: /.{8,}/,
    upper: /[A-Z]/,
    lower: /[a-z]/,
    digit: /\d/,
    special: /[^A-Za-z0-9]/
  };
  Object.entries(rules).forEach(([id, regex]) => {
    const el = document.getElementById(id);
    if (!el) return;
    if (regex.test(pw)) el.classList.add('valid');
    else el.classList.remove('valid');
  });
}

// 3) Şifre göster/gizle
function togglePassword() {
  const inp = document.getElementById('password');
  const icon = document.getElementById('togglePasswordIcon');
  if (!inp || !icon) return;

  const isHidden = inp.type === 'password';
  inp.type = isHidden ? 'text' : 'password';
  icon.classList.replace(isHidden ? 'bi-eye' : 'bi-eye-slash',
                        isHidden ? 'bi-eye-slash' : 'bi-eye');
}

// 4) Giriş kontrolü ve yönlendirme
function login() {
  const pw = document.getElementById('password').value;
  const checks = [/.{8,}/, /[A-Z]/, /[a-z]/, /\d/, /[^A-Za-z0-9]/];
  if (!checks.every(rx => rx.test(pw))) {
    alert('Şifre en az 8 karakter, büyük/küçük harf, rakam ve özel karakter içermeli.');
    return;
  }
  // Başarılıysa formu temizle ve kriterleri sıfırla
  document.getElementById('loginForm').reset();
  document.querySelectorAll('#passwordCriteria li').forEach(li => li.classList.remove('valid'));

  // Yönlendir
  window.location.href = 'preferences.html';
}

// 5) Çıkış: giriş sayfasına dön
function logout() {
  window.location.href = 'index.html';
}

// 6) Chart.js render (sadece stats.html’de)
function renderStatsChart() {
  const ctx = document.getElementById('genreChart')?.getContext('2d');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Pop','Rock','Caz','Klasik'],
      datasets: [{
        label: 'Dinlenme %',
        data: [40,30,15,15],
        backgroundColor: ['#ff6384','#36a2eb','#cc65fe','#ffce56']
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, max: 100,
             ticks: {
               // Tema renk uyumu
               color: getComputedStyle(document.body).color
             }
        },
        x: {
          ticks: {
            color: getComputedStyle(document.body).color
          }
        }
      }
    }
  });
}

// 7) Sayfa yüklendiğinde tema ve animasyon/grafik tetikle
window.addEventListener('DOMContentLoaded', () => {
  // Kayıtlı temayı uygula
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-bs-theme', saved);
  document.body.setAttribute('data-theme', saved);
  const icon = document.getElementById('themeIcon');
  if (icon) {
    icon.className = saved === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
  }

  // Grafiği çiz
  renderStatsChart();

  // Şifre inputuna canlı doğrulama bağla
  const pwInput = document.getElementById('password');
  if (pwInput) {
    pwInput.addEventListener('input', validatePassword);
  }
});
