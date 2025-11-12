// Background service worker (handles messages & context menu)
let API_KEY = null;

// Create context menu on install
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'summarize-selection',
    title: 'Summarize selection (Insightify)',
    contexts: ['selection'],
  });
});

// When user right-clicks and selects “Summarize selection”
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === 'summarize-selection') {
    const text = info.selectionText;
    chrome.tabs.sendMessage(tab.id, { type: 'OPEN_POPUP_WITH_TEXT', text });
  }
});

// 🔥 Single unified message listener
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'HIGHLIGHT') {
    // Save last highlighted text for popup use
    chrome.storage.local.set({ lastSelection: message.text });
    return;
  }

  if (message.type === 'CALL_API') {
    (async () => {
      try {
        const resp = await fetch(message.url, {
          method: message.method || 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...message.headers,
          },
          body: message.body ? JSON.stringify(message.body) : undefined,
        });

        if (!resp.ok) {
          const errText = await resp.text();
          sendResponse({
            success: false,
            error: `Backend returned ${resp.status}: ${errText}`,
          });
          return;
        }

        const data = await resp.json();
        sendResponse({ success: true, data });
      } catch (err) {
        sendResponse({ success: false, error: err.message });
      }
    })();

    // Keep the message channel open for async sendResponse
    return true;
  }
});
