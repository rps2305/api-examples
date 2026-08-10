const venueWindow = document.querySelector('.venue-window');
const venuePause = document.querySelector('.venue-pause');

if (venueWindow && venuePause) {
  venuePause.addEventListener('click', () => {
    const paused = venueWindow.dataset.paused === 'true';
    venueWindow.dataset.paused = String(!paused);
    venuePause.setAttribute('aria-pressed', String(!paused));
    venuePause.textContent = paused ? 'Pauzeer bewegende locaties' : 'Hervat bewegende locaties';
  });
}
