import { useEffect, useState } from "react";

import { getSession, login, logout } from "./api/auth";
import Dashboard from "./components/Dashboard";
import LoginForm from "./components/LoginForm";

export default function App() {
  const [user, setUser] = useState(null);
  const [checkingSession, setCheckingSession] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getSession()
      .then((payload) => {
        if (payload.authenticated) {
          setUser(payload.user);
        }
      })
      .catch(() => {
        setError("감시 API에 연결할 수 없습니다.");
      })
      .finally(() => {
        setCheckingSession(false);
      });
  }, []);

  async function handleLogin(username, password) {
    setError("");
    try {
      const payload = await login(username, password);
      setUser(payload.user);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function handleLogout() {
    try {
      await logout();
    } finally {
      setUser(null);
      setError("");
    }
  }

  if (checkingSession) {
    return <main className="center-screen">로그인 상태를 확인하는 중입니다.</main>;
  }

  if (!user) {
    return <LoginForm onLogin={handleLogin} error={error} />;
  }

  return <Dashboard user={user} onLogout={handleLogout} />;
}
