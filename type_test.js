(function() {
  const input = document.querySelector('[contenteditable="true"]');
  if (input) {
    input.innerHTML = "Testing full automation";
    input.dispatchEvent(new Event('input', { bubbles: true }));
    return "typed";
  }
  return "not_found";
})()