/* Generic Confirm func */
function confirm2(heading, question, cancelButtonTxt, okButtonTxt, callback) {
    var confirmModal = 
        $('<div class="modal fade">' +        
            '<div class="modal-dialog">' +
            '<div class="modal-content">' +
            '<div class="modal-header">' +
            '<h3>' + heading +'</h3>' +
            '<a class="close" data-dismiss="modal" >&times;</a>' +
            '</div>' +

            '<div class="modal-body">' +
            '<p>' + question + '</p>' +
            '</div>' +

            '<div class="modal-footer">' +
            '<a href="#!" class="btn" data-dismiss="modal">' + 
                cancelButtonTxt + 
            '</a>' +
            '<a href="#!" id="okButton" class="btn btn-primary">' + 
                okButtonTxt + 
            '</a>' +
            '</div>' +
            '</div>' +
            '</div>' +
        '</div>');

    confirmModal.find('#okButton').click(function(event) {
        callback();
        confirmModal.modal('hide');
    }); 

    confirmModal.modal('show');    
};  
/* END Generic Confirm func */
