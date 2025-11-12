const BACKEND_URL = 'http://127.0.0.1:8000'; // change to deployed URL in production
const BACKEND_API_KEY = 'insightify_api_key';

async function loadSelection() {
  const data = await chrome.storage.local.get('lastSelection');
  const txt = data.lastSelection || '';
  document.getElementById('selectedText').innerText = txt || 'No selection yet.';
}

async function callBackend(text, mode) {
  const s = await chrome.storage.sync.get(API_KEY_STORAGE);
  const apiKey = s[API_KEY_STORAGE];
  const headers = { 'Authorization': `Bearer ${apiKey || ''}` };
  const body = { text, mode };

  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(
      {
        type: 'CALL_API',
        url: `${BACKEND_URL}/summarize`,
        method: 'POST',
        headers,
        body,
      },
      (resp) => {
        if (!resp || !resp.data) {
          reject(new Error('No response from backend.'));
        } else {
          resolve(resp.data);
        }
      }
    );
  });
}

window.addEventListener('load', async () => {
  await loadSelection();
  document.getElementById('summarizeBtn').addEventListener('click', async () => {
    const text = document.getElementById('selectedText').innerText;
    if (!text || text === 'No selection yet.') {
      return alert('Select text on the page first.');
    }

    document.getElementById('result').innerText = 'Thinking...';

    try {
      const mode = document.getElementById('modeSelect').value;
      const resp = await callBackend(text, mode);

      // ✅ Handle both possible response formats
      const output =
        resp.summary?.summary || resp.summary || JSON.stringify(resp, null, 2);

      document.getElementById('result').innerText = output;
    } catch (e) {
      document.getElementById('result').innerText = 'Error: ' + e.message;
    }
  });
});
