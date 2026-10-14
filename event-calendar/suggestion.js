const suggestionForm = document.querySelector('#suggestion-form');
const suggestionStatus = document.querySelector('#suggestion-status');
let suggestionToken = '';

async function refreshSuggestionToken() {
  const response = await fetch('/api/suggestions/token', { cache: 'no-store', credentials: 'same-origin' });
  if (!response.ok) throw new Error('token unavailable');
  suggestionToken = (await response.json()).token;
}

if (suggestionForm) {
  refreshSuggestionToken().catch(() => {
    suggestionStatus.textContent = 'De ideeënbus is tijdelijk niet beschikbaar.';
  });
  suggestionForm.addEventListener('submit', async event => {
    event.preventDefault();
    const submitButton = suggestionForm.querySelector('button[type="submit"]');
    const fields = new FormData(suggestionForm);
    submitButton.disabled = true;
    suggestionStatus.textContent = 'Suggestie versturen…';
    try {
      if (!suggestionToken) await refreshSuggestionToken();
      const response = await fetch('/api/suggestions', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token: suggestionToken,
          name: fields.get('name'),
          email: fields.get('email'),
          category: fields.get('category'),
          message: fields.get('message'),
          website: fields.get('website'),
        }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Versturen mislukt.');
      suggestionForm.reset();
      suggestionStatus.textContent = 'Bedankt! Je suggestie is naar Ronald verstuurd.';
      suggestionToken = '';
      await refreshSuggestionToken();
    } catch (error) {
      suggestionStatus.textContent = error.message || 'Versturen mislukt. Probeer het later opnieuw.';
      suggestionToken = '';
      refreshSuggestionToken().catch(() => {});
    } finally {
      submitButton.disabled = false;
    }
  });
}
