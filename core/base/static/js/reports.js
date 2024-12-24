let occurrencesData = document.getElementById('occurrences-data').value
const ctx = document.getElementById('chart-occurrences')
new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Em Aberto', 'Em Execução', 'Resolvido', 'Não Resolvido', 'Cancelado'],
        datasets: [{
            data: JSON.parse(occurrencesData),
            backgroundColor: [
                '#5a6268',
                '#0d6efd',
                '#28a745',
                '#ffc107',
                '#dc3545'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
})
let totalMessages = document.getElementById('total-messages').value
console.log(totalMessages)
let dateMessages = document.getElementById('date-messages').value
const ctx2 = document.getElementById('chart-messages')
new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: JSON.parse(dateMessages.replace(/'/g, '"')),
        datasets: [{
            label: 'Últimos 5 Dias',
            data: JSON.parse(totalMessages),
            backgroundColor: [
                '#0d6efd',
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
})