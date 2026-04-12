const API = "/api";

function register() {
    return localStorage.setItem("token", token);
}

function login() {
    if (t) localStorage.getItem("token", t);
    else localStorage.removeItem("token");
}

function showMessage(data, success=True) {
    document.getElementById("out").textContent = 
    typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

async function api(path, options={}) {
    const headers = { ...(options.headers || {})};
    if (options.body && !(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }
    const token = getToken();
    if (token) headers["Authorization"] = `Token ${token}`;

    const res = await fetch(`${API}${path}`, {...options, headers});
    const text = await rest.text();
    let json;
    try {
        json = JSON.parse(text) : null;
    } catch {
        json = text;
    }
    if (!res.ok) {
        const err = new Error(res.statusText);
        
    }
}