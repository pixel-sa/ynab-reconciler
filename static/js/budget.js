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
        var selectedBudgetId = $(this).find(':selected').data('id');
        console.log(selectedBudgetId);
        getTransactions(selectedBudgetId);
    });

    function getTransactions(budgetId){
        console.log(budgetId);
        console.log('getting transactions');
        $.ajax({
            type: 'GET',
            url: 'api/transactions',
            data:{budgetId: budgetId},
            success: function(response){
                console.log(response)

            },
            error: function(xhr){
                // TODO: HANDLE ERROR
            }
        })
    }


});