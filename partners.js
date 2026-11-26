'use strict';
const form = document.getElementById('partner-form');
document.querySelectorAll('[data-interest]').forEach(link => link.addEventListener('click', () => {
  form.elements.interest.value = link.dataset.interest;
}));
form.addEventListener('submit', event => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const data = new FormData(form);
  const body = `Name: ${data.get('name')}\nCompany: ${data.get('company')}\nReply email: ${data.get('email')}\nInterest: ${data.get('interest')}\n\n${data.get('message')}`;
  document.getElementById('prepared-message').value = body;
  document.getElementById('email-status').textContent = 'Your message is prepared, not sent. Review and send it in your email app. If no app opens, copy the prepared message and email ahogentertainment@gmail.com.';
  window.location.href = `mailto:ahogentertainment@gmail.com?subject=${encodeURIComponent('Shuttlebug — ' + data.get('interest') + ' inquiry')}&body=${encodeURIComponent(body)}`;
});
