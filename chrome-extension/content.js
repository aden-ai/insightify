// Runs in page context — listens for mouseup and sends selected text to background
function getSelectedText() {
const s = window.getSelection();
return s ? s.toString().trim() : "";
}


document.addEventListener("mouseup", () => {
const text = getSelectedText();
if (text.length > 0) {
chrome.runtime.sendMessage({ type: 'HIGHLIGHT', text });
}
});