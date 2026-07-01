(function (e) {
    'use strict';
    $('#summernote').summernote({
        height: 300,
        focus: false,
    });
    $('#summernote_ar').summernote({
        height: 300,
        focus: false,
        lang: 'en-US',
        callbacks: {
            onInit: function() {
                // Enable RTL for Arabic editor
                var $editor = $('#summernote_ar').next('.note-editor');
                $editor.find('.note-editable').attr('dir', 'rtl');
            }
        }
    });
})();