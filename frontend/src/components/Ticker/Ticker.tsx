import { useState, useEffect } from "react";
import "./Ticker.css";

export function Ticker() {
  const [ticker, setTicker] = useState("");

  useEffect(() => {
    const handlePywebviewReady = () => {
      if (!window.pywebview.state) {
        window.pywebview.state = {};
      }

      // @ts-expect-error This is a custom state
      window.pywebview.state.setTicker = setTicker;
    };

    if (window.pywebview) {
      handlePywebviewReady();
    } else {
      window.addEventListener("pywebviewready", handlePywebviewReady);
    }

    return () => {
      window.removeEventListener("pywebviewready", handlePywebviewReady);
    };
  }, []);

  return (
    <div className="ticker-container">
      <h1>Welcome to pywebview!</h1>

      <em>
        You can freely communicate between Javascript with Python without a HTTP
        server. This value, for example, is being generated by Python code:
      </em>
      <strong>{ticker}</strong>
    </div>
  );
}
