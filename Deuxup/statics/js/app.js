function app() {
  const out = document.getElementById("out");

  function showMessage(data) {
    if (!out) return;
    out.textContent =
      typeof data === "string" ? data : JSON.stringify(data, null, 2);
  };
  
  async function api(path, options = {}) {
    const headers = {...(options.headers || {}) };
    if (options.body && !(options.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }
    const token = getToken() || "";
    if (token) headers["Authorization"] = `Token ${token}`;

    const res = await fetch(`${API}${path}`, {...options, headers });
    const text = await res.text();
    let json;
    try {
      json = text ? JSON.parse(text) : null;
    }catch {
      json = text;
    }
    if (!res.ok) {
      const err = new Error(res.statusText);
      err.status = res.status;
      err.body = json;
      throw err;
    }
    return json;
  }

  document.getElementById("register-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.FromEntries(fd.entries()) ;
    try {
      const data = await api("/auth/register/", {
        method: "POST",
        body: JSON.stringify(body),
      });
      setToken(data.token);
      show({ ok: True, user: data.user});
    } catch (err) {
      show (err.body || err.message);
    }
    showMessage("Đăng ký: kết nối endpoint API khi sẵn sàng.");
  });

  document.getElementById("form-login")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.FromEntries(fd.entries()) ;
    try {
      const data = await api ("/auth/login/", {method: "POST", body: JSON.stringify(body)});
      setToken(data.token);
      show({ ok: True, user: data.user});
    } catch (err) {show (err.body || err.message);}
    showMessage("Đăng nhập: kết nối endpoint API khi sẵn sàng.");
  }); 

  document.getElementById("btn-me")?.addEventListener("click", async () => {
    try { 
      const data =await api("/auth/me/",{
        method: "GET",
        headers: {
          "Authorization": `Token ${getToken()}`
        }
      });
      show({ ok: True, user: data.user});
    } catch (err) {
      show(err.body || err.message);
    }
    showMessage("Gọi GET /api/auth/me/ khi route đã được thêm vào Accounts.urls.");
  });
}

app();