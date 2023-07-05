const handleToggle = (element) => {
  const summaryText = element.getElementsByClassName('atlas-summary-text')[0]

  if (summaryText.textContent === 'View video transcript') {
    summaryText.textContent = 'Hide video transcript'
  } else {
    summaryText.textContent = 'View video transcript'
  }
}

const detailsElements = document.querySelectorAll('[data-transcript-toggle]')
detailsElements.forEach((element) =>
  element.addEventListener('toggle', () => handleToggle(element))
)
