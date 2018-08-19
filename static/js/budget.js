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
    console.log("hello!")

    $(document).on('change', '#budget-select', function() {
        $("#account-select-div").html("");

        var selectedBudgetId = $(this).find(':selected').data('id');
        console.log(selectedBudgetId);
        getAccounts(selectedBudgetId);
    });

    $(document).on('change', '#account-select', function() {
        $("#balance-div").html("");

        var selectedBudgetId = $(this).find(':selected').data('budgetid');
        var selectedAccountId = $(this).find(':selected').data('accountid');
        var selectedBalance = $(this).find(':selected').data('balance');

        displayAccountBalance(selectedBalance);


        // getTransactions(selectedBudgetId, selectedAccountId, selectedBalance);
    });

    function displayAccountBalance(balance){
        console.log("dispaying account balance!!!");
        html = "";
        html += '<div class="form-group">';
        html += '<label for="account-balance">Please enter correct account balance</label>';
        html += '<input type="text" class="form-control" id="account-balance" placeholder="Current account balance">';
        // html += '<small id="emailHelp" class="form-text text-muted">Your most up to date account balance is'+ balance +'</small>';
        html += '</div>';
        
        html += '<form id="upload-file" method="post" enctype="multipart/form-data">';
        html += '<fieldset>';
        html += '<label for="file">Select a file</label>';
        html += '<input name="file" type="file">';
        html += '</fieldset>';
        html += '<fieldset>';
        html += '<button type="submit" class="btn btn-primary" id="upload-file-btn">Submit!</button>';
        html += '</fieldset>';
        html += '</form>';



        // html += '<form id="upload-csv-form" method="post" enctype="multipart/form-data">';
        // html += '<div class="form-group">';

        // html += '<div class="input-group mb-3">';
        // html += '<div class="input-group-prepend">';
        // html += '<span class="input-group-text" id="inputGroupFileAddon01">Upload</span>';
        // html += '</div>';
        // html += '<div class="custom-file">';
        // html += '<input type="file" class="custom-file-input" id="inputGroupFile01" aria-describedby="inputGroupFileAddon01">';
        // html += '<label class="custom-file-label" for="inputGroupFile01">Choose file</label>';
        // html += '</div>';
        // html += '</div>';
        // html += '</div>';
        // html += '<button type="submit" class="btn btn-primary" id="upload-file-btn">Submit</button>';
        // html += '</form>';

        $("#balance-div").html(html);
        dispalyFileName();
        // uploadCsvFile();

        $('#upload-file-btn').click(function() {
            var form_data = new FormData($('#upload-file')[0]);
            $.ajax({
                type: 'POST',
                url: '/upload/csv',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function(data) {
                    console.log('Success!');
                },
            });
        });

    }

    function dispalyFileName(){
        $('.custom-file-input').on('change',function(){
            console.log("display!!!");
            var fileName = $(this).val();
            console.log(fileName);
            $(this).next('.custom-file-label').html(fileName);
        })    
    }

    function uploadCsvFile(){

        $(document).on('click', '#upload-file-btn', function(event) {
            console.log(event);
            var form_data = new FormData($('#upload-file')[0]);
            $.ajax({
                type: 'POST',
                url: '/upload/csv',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(response) {
                    return false;
                    event.preventDefault();
                    console.log(response);
                },
            });
        

            return false;
        });

    }

    function getAccounts(budgetId){
        console.log(budgetId);
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

    function getTransactions(budgetId, accountId, balance){
        console.log('getting transactions');
        console.log(budgetId);
        console.log(accountId)
        console.log(balance)
        $.ajax({
            type: 'GET',
            url: 'api/transactions',
            data:{budgetId: budgetId, accountId: accountId, balance: balance},
            success: function(response){
                console.log(response)

            },
            error: function(xhr){
                // TODO: HANDLE ERROR
            }
        })
    }


});