const shadowPlugin = {
    id: 'shadowPlugin',
    afterDatasetsDraw: function(chart, easing) {
        var ctx = chart.ctx;
        chart.data.datasets.forEach(function(dataset, i) {
            var meta = chart.getDatasetMeta(i);
            if (!meta.hidden) {
                meta.data.forEach(function(element, index) {
                    // Draw the shadow under each point
                    ctx.fillStyle = '#056d93'; // Shadow color
                    ctx.shadowColor = '#056d93'; // Same color as the line
                    ctx.shadowBlur = 10;
                    ctx.shadowOffsetX = 0;
                    ctx.shadowOffsetY = 0;
                    ctx.beginPath();
                    ctx.arc(element.x, element.y, element.radius, 0, Math.PI * 2);
                    ctx.fill();
                });
            }
        });
    }
};

// Register the plugin
Chart.register(shadowPlugin);

// Chart initialization
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'],
        datasets: [{
            label: 'Total Balance',
            data: [9455, 2328, 6639, 5419, 3645, 2098, 8505, 4709, 8181, 9762, 3647, 7475, 5673, 2859, 7447, 2229, 1910, 8149, 7383, 3944, 8297, 5862, 7674, 5735, 7148, 2606, 1839, 3828, 3345, 3607, 7443, 10000],
            borderColor: '#a45cf6',
            borderWidth: 3.5,
            lineTension: 0.5,
            fill: true,
            backgroundColor: 'rgba(164, 92, 246, 0.09)', // Gradient fill under the line
            pointRadius: 0.5,
            pointBackgroundColor: '#079c4b',
            pointBorderColor: 'white',
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
                labels: {
                    color: 'white',
                    font: {
                        family: 'Poppins' // Poppins font for legend labels
                    }
                }
            },
            tooltip: {
                callbacks: {
                    title: function(tooltipItems) {
                        // Assuming you want to map specific days to months for demonstration
                        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                        // Use the first tooltip item to determine the label
                        let day = tooltipItems[0].label;
                        // Example mapping: every month is 30 days for simplicity, adjust according to your data
                        let monthIndex = Math.floor(day / 30); // This will work for a simplified case
                        // Return the month name; adjust logic as needed for accurate mapping
                        return monthNames[monthIndex];
                    },
                    label: function(context) {
                        var label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label +=  context.parsed.y + ' $' ;
                        }
                        return label;
                    }
                },
                enabled: true,
                mode: 'index',
                intersect: false,
                bodyFont: {
                    family: 'Poppins' // Poppins font for tooltips
                }
            }
        },
        scales: {
            y: {
                grid: {
                    color: '#f5f5f521',
                },
                ticks: {
                    color: '#ffffff',
                    callback: function(value) {
                        return value + ' $';
                    },
                    font: {
                        family: 'Poppins' // Poppins font for y-axis labels
                    }
                }
            },
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0)',
                    borderColor: 'rgba(255, 255, 255, 1)'
                },
                ticks: {
                    color: '#f5f5f521',
                    font: {
                        family: 'Poppins' // Poppins font for x-axis labels
                    }
                }
            }
        }
    }
});

function addAndRemove(lst, newValue) {
    lst.push(newValue); // Add the new balance to the end
    lst.shift(); // Remove the oldest data point
    return lst;
}

function newDayUpdateChart(newBalance) {
    console.log("Updating New Day Chart...");

    // Retrieve the current data array
    var currentData = myChart.data.datasets[0].data;

    // Remove the oldest data point by shifting the array
    currentData.shift();

    // Add the new balance to the end of the array
    currentData.push(newBalance);

    // Update the dataset with the modified data array
    myChart.data.datasets[0].data = currentData;

    // Update the chart
    myChart.update();
}

function updateChart(newBalance) {
    console.log("Updating Chart current point...");

    myChart.data.datasets[0].data[31] = newBalance
    var newData = myChart.data.datasets[0].data;

    myChart.data.datasets[0].data = newData;
    myChart.update();
}

function updateDashboard() {
    ajaxRequest('GET', '/getDashboard/', null, function(response) {
        if (response.success) {
            var newBalance = response["dashboard"].balance;
            var newObjectif = response["dashboard"].objectif;
            var newProfits = response["dashboard"].profits;
            var newLosses = response["dashboard"].losses;
            var newProfitsPercentage = response["dashboard"].profits_percentage;
            var newLossesPercentage = response["dashboard"].losses_percentage;
            var btc = response["dashboard"].btc;
            var eth = response["dashboard"].eth;
            var sol = response["dashboard"].sol;

            console.log(btc, eth, sol)

            updateChart(newBalance);
            newDayUpdateChart(newBalance)

            var balanceElement = document.querySelector('.balance');
            var objectifElement = document.querySelector('.objectif');
            var profitsElement = document.querySelector('.profits');
            var lossesElement = document.querySelector('.losses');
            var profitsPercentageElement = document.querySelector('.icons-up-green');
            var lossesPercentageElement = document.querySelector('.icons-up-red');
            var lossesPercentageBtcElement = document.querySelector('.percentage-down-up.btc');
            var lossesPercentageEthElement = document.querySelector('.percentage-down-up.eth');
            var lossesPercentageSolElement = document.querySelector('.percentage-down-up.ltc');
            var lossesBtcElement = document.querySelector('.price-v.btc');
            var lossesEthElement = document.querySelector('.price-v.eth');
            var lossesSolElement = document.querySelector('.price-v.ltc');

            balanceElement.textContent = '$' + newBalance;
            objectifElement.textContent = '$' + newObjectif;
            profitsElement.textContent = '+$' + newProfits;
            lossesElement.textContent = '-$' + newLosses;
            profitsPercentageElement.textContent = '%' + newProfitsPercentage;
            lossesPercentageElement.textContent = '-%' + newLossesPercentage;
            lossesPercentageBtcElement.textContent = '%' + btc[1].toFixed(2);
            lossesPercentageEthElement.textContent = '%' + eth[1].toFixed(2);
            lossesPercentageSolElement.textContent = '%' + sol[1].toFixed(2);
            lossesBtcElement.textContent = '$' + btc[0];
            lossesEthElement.textContent = '$' + eth[0];
            lossesSolElement.textContent = '$' + sol[0];
        }
    }, null, true, "Update dashboard", null)

}

function updateRanking() {
    ajaxRequest('GET', '/getRanking/', null, function(response) {
        if (response.top_users.length > 0) {
            var htmlContent = '';
            response.top_users.forEach(function(user) {
                htmlContent += '<div class="user-ranking-list">';
                htmlContent += '<div class="profile-user-ranking">';
                console.log(`assets/top${user.rankIco}.svg`)
                htmlContent += `<img src="../static/assets/top${user.rankIco}.svg" alt="Rank" class="ranking-pic">`;
                htmlContent += '<img class="profile-user-pic" src=' + user.pfp + ' alt="">';
                htmlContent += '<span class="profile-user-name">' + user.username + '</span>';
                htmlContent += '</div>';
                htmlContent += '<div class="ranking-amount-container">';
                htmlContent += '<span class="amount-trade">$' + user.balance + '</span>';
                htmlContent += '</div>';
                htmlContent += '</div>';
            });
            $('.ranking-user').html(htmlContent);
        }
    }, null, true, "Update ranking", null)
}

function updateTopUser() {
    var memberOfMonth = document.querySelector('.name-user');
    var memberOfMonthPfp = document.querySelector('.user-picture')
    ajaxRequest('GET', '/getTopUser/', null, function(response) {
        if (response.success) {
            console.log(response)
            memberOfMonth.innerText = response.top_user_username;
            memberOfMonthPfp.src = response.top_user_pfp

            var badgesHTML = '';
            response.top_user_badgesList.forEach(function(badge) {
                badgesHTML += `<img class="profile-user-badges" src="${badge.icon}" alt="${badge.title}">`;
            });
        
            // Append the generated HTML for badges to the .badges-user div
            document.querySelector('.badges-user').innerHTML = badgesHTML;
        }
    }, null, true, "Updating member of the month", null)
}

function updateTransactions() {
    console.log("Updating Transactions...");
    var transactionHistoryElement = document.querySelector('.transactions-history');
    ajaxRequest('GET', '/getTransactions/', null, function(response) {
        if (response.success) {
            transactionHistoryElement.innerHTML = '';
        
            for (let i = 0; i < Math.min(4, response.transactions.length); i++) {
                let transaction = response.transactions[i];
                // Assign class based on transaction type
                var amountClass = transaction.type === 'profit' ? 'profit-background' : 'loss-background';
                var auntClass = transaction.type === 'profit' ? 'transaction-info-text' : 'transaction-info-text-loss';
            
                // Build HTML for badges
                var badgesHTML = '';
                transaction.badges.forEach(function(badge) {
                    badgesHTML += `<img class="profile-user-badges" src="${badge.icon}" alt="${badge}">`;
                });
            
                var transactionHTML = `
                    <div class="history-user-transc">
                        <div class="ianloine">
                            <div class="profile-picture-container">
                                <img class="profile-user-transaction" src="${transaction.pfp}" alt="">
                            </div>
                            <div class="informations-user">
                                <div class="name-fser">
                                    <span class="foll">${transaction.user}</span>
                                    ${badgesHTML} <!-- Render badges here -->
                                </div>
                                <div class="date-badges">
                                    ${transaction.date}
                                </div>
                            </div>
                        </div>
                        <div class="data-transaction-info">
                            <div class="data-transaction">
                                <span class="data-transaction-text">
                                    ${transaction.pair} <span class="transaction-info-text ${auntClass}">${transaction.type}</span>
                                </span>
                            </div>
                            <div class="transaction-amount-container ${amountClass}">
                                <span class="amount-trade">${transaction.amount} $</span>
                            </div>
                        </div>
                    </div>
                `;
                transactionHistoryElement.insertAdjacentHTML('beforeend', transactionHTML);
            }
        }
    }, null, true, "Update transactions", null)
}


document.addEventListener('DOMContentLoaded', () => {
    var addTransactionButton = document.querySelector('.THEbutton');
    addTransactionButton.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default form submission behavior

        // Serialize the form data
        var formData = new FormData(document.querySelector('form'));
        ajaxRequest('POST', '/add_transaction/', formData, function(response) {
            if (response.success) {
                console.log(response);
                // Optionally, you can redirect or show a success message here
                // remove opened class from div with modale 
                $('.modale').removeClass('opened');
                // Update the dashboard with the new transaction data
                updateDashboard();
                updateTransactions();
            }
        }, null, true, "add transaction", null)
    });


    updateChart()
    setInterval(updateChart, 1000);

    updateDashboard()
    setInterval(updateDashboard, 10000);

    /* updateTopUser()
    setInterval(updateTopUser, 10000); */

    /* updateRanking()
    setInterval(updateRanking, 10000); */

    /* updateTransactions();
    setInterval(updateTransactions, 10000); */


    $('.openmodale').click(function (e) {
        e.preventDefault();
        $('.modale').addClass('opened');
    });
    $('.closemodale').click(function (e) {
        e.preventDefault();
        $('.modale').removeClass('opened');
    });
    $('#chooseFile').bind('change', function () {
        var filename = $("#chooseFile").val();
        if (/^\s*$/.test(filename)) {
            $(".file-upload").removeClass('active');
            $("#noFile").text("No file chosen..."); 
        } else {
            $(".file-upload").addClass('active');
            $("#noFile").text(filename.replace("C:\\fakepath\\", "")); 
        }
    });

    /* ROLL ANIMATION HERE */
});