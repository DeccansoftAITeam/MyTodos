import { useState, useEffect } from 'react';

export default function DateTime() {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="datetime">
      <span className="datetime-date">{now.toLocaleDateString()}</span>
      <span className="datetime-time">{now.toLocaleTimeString()}</span>
    </div>
  );
}
