// var BUDGET = {
//     runtime:{
//         message: ''
//     },

//     init:function(message){
//         console.log('WHHHHHAT!')
//         BUDGET.runtime.message = message
//         console.log(BUDGET.runtime.message)
//     }
// }

$(document).ready(function(){
    console.log("hello!");

    function hideAlertMessage(){
        $("#alert-message").hide();
    }

    initialQuestion();

    function initialQuestion(){
        var html = "";
        html += '<div class="form-group">';
        html += '<label>Does your transaction csv have separate columns for debits and credits?</label>';
        html += '<div class="form-check">';

        html += '<label class="form-check-label">';
        html += '<input type="radio" class="form-check-input" name="optradio" value="yes">Yes';
        html += '</label>';
        html += '</div>';
        html += '<div class="form-check">';
        html += '<label class="form-check-label">';
        html += '<input type="radio" class="form-check-input" name="optradio" value="no">No';
        html += '</label>';
        html += '</div>';
        html += '</div>';  
        
        $("#initial-question").html(html);
        initialQuestionEvents();
    }

    function initialQuestionEvents(){
        $('input[name=optradio]').change(function(){
            var radioValue = $( 'input[name=optradio]:checked' ).val();
            if(radioValue == "yes"){
                $("#main, #budget-select-div").show();
                hideAlertMessage();
            } else if (radioValue == "no") {
                $("#main").hide();
                $("#alert-message").html("Sorry! We don't support this format yet! Help us out by submitting <a target='_blank' href='https://goo.gl/forms/62b01aknc1epECWb2'>this form!</a>").show();
            }
        }); 
    }

    $(document).on('change', '#budget-select', function() {
        $("#account-select-div").html("");
        var selectedBudgetId = $(this).find(':selected').data('id');
        getAccounts(selectedBudgetId);
    });

    function getAccounts(budgetId){
        console.log('getting accounts');
        $.ajax({
            type: 'GET',
            url: 'api/accounts',
            data:{budgetId: budgetId},
            success: function(response){
                console.log(response);
                populateAccounts(response,budgetId)
            },
            error: function(xhr){
                // TODO: HANDLE ERROR
            }
        })
    }

    function populateAccounts(accountList, budgetId){
        console.log("populating accounts!")

        accounts = accountList['data']['accounts']
        var html = "";
        html += '<label for="account-select">Select Account to Reconcile</label>';
        html += '<select class="form-control" id="account-select">';
        html += '<option disabled selected>Choose One</option>';
        
        accounts.forEach(element => {
            html += '<option data-budgetid="'+ budgetId +'" data-balance="'+element['balance'] +'" data-accountid="'+ element['id'] +'">'+element['name'] +'</option>';   
        });

        html += '</select>';

        $("#account-select-div").html(html);
    }


    $(document).on('change', '#account-select', function() {
        $("#balance-div").html("");
        var selectedBudgetId = $('#budget-select').find(':selected').data('id');
        var selectedAccountId = $(this).find(':selected').data('accountid');
        var selectedBalance = $(this).find(':selected').data('balance');
        
        displayBankOptions();
        // displayUploadOption(selectedBalance);
        getTransactions(selectedBudgetId, selectedAccountId);
    });

    function displayBankOptions(){
        html = "";
        html += '<div class="form-group">';
        html += '<label for="bank-select">Select Bank (This is so we know your csv format!)</label>';
        html += '<select class="form-control" id="bank-select">';
        html += '<option disabled selected> Select One</option>';
        html += '<option value="ibc"> International Bank of Commerce (IBC) </option>';
        html += '<option value="nfcu"> Navy Federal Credit Union (NFCU) </option>';
        html += '<option value="other"> Other</option>';
        html += '</select>';
        html += '</div>';

        $("#bank-div").html(html);
        bankOptionEvents();      
    }

    function bankOptionEvents(){
        $(document).on('change', '#bank-select', function() {    
            var selectedBank = this.value

            if (selectedBank == "nfcu" || selectedBank == "ibc"){
                displayUploadOption();
            } else {    
                manualMapping();
            }

    
            // displayUploadOption(selectedBalance);
            // getTransactions(selectedBudgetId, selectedAccountId, '1500');
        });
    }



    function manualMapping(){
        $("#alert-message").html("Sorry! We don't support additional banks yet! Help us out by submitting <a target='_blank' href='https://goo.gl/forms/62b01aknc1epECWb2'>this form!</a>").show();

        var html = "";
        html += '<label>Does your transaction csv have separate columns for debits and credits?</label>';
        html += '<label for="account-select">Select Account to Reconcile</label>';
        html += '<select class="form-control" id="account-select">';
        html += '<option disabled selected>Choose One</option>';
        html += '</select>';       
    }

    function displayUploadOption(){
        console.log("dispaying account balance!!!");
        hideAlertMessage();

        html = "";

        // html += '<div class="form-group">';
        // html += '<label for="account-balance">Please enter correct bank account balance</label>';
        // html += '<input type="text" class="form-control" id="account-balance" placeholder="account balance">';
        // html += '</div>';
        
        html += '<form id="upload-file" action="upload/csv" method="post" enctype="multipart/form-data">';
        html += '<fieldset>';
        html += '<label for="file">Upload CSV file</label>';
        html += '<input name="file" type="file">';
        html += '</fieldset>';
        html += '<fieldset>';
        html += '<input type="submit" class="btn btn-primary" id="upload-file-btn" value="Upload CSV"></input>';
        html += '</fieldset>';
        html += '</form>';
        
        $("#balance-div").html(html);
    }

    function getTransactions(budgetId, accountId){
        console.log('getting transactions');
    
        $.ajax({
            type: 'GET',
            url: 'api/transactions',
            data:{budgetId: budgetId, accountId: accountId},
            success: function(response){
                console.log(response)

            },
            error: function(xhr){
                // TODO: HANDLE ERROR
            }
        })
    }

});