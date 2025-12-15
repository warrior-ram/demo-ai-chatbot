import React from 'react';
import ReactDOM from 'react-dom/client';
import ChatWidget from '../components/chat/ChatWidget';
// import styleText from '../app/globals.css?inline'; // Vite inline import

const WIDGET_ID = 'ai-chat-widget-root';

function init() {
    // Find script tag to get config
    const script = document.currentScript as HTMLScriptElement;
    const botId = script?.dataset?.botId ? parseInt(script.dataset.botId) : 1;

    // Create host element
    let host = document.getElementById(WIDGET_ID);
    if (!host) {
        host = document.createElement('div');
        host.id = WIDGET_ID;
        document.body.appendChild(host);
    }

    // Create Shadow DOM
    const shadow = host.attachShadow({ mode: 'open' });

    // Inject Styles
    // const style = document.createElement('style');
    // style.textContent = styleText;
    // shadow.appendChild(style);

    // Mount React
    const mountPoint = document.createElement('div');
    shadow.appendChild(mountPoint);

    const root = ReactDOM.createRoot(mountPoint);
    root.render(
        <React.StrictMode>
            <div className="fixed bottom-4 right-4 z-50">
                <ChatWidget botId={botId} />
            </div>
        </React.StrictMode>
    );
}

if (document.readyState === 'complete') {
    init();
} else {
    window.addEventListener('load', init);
}
