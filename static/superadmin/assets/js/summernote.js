(function (e) {
    'use strict';
    
    var handlePaste = function (e) {
        var bufferText = ((e.originalEvent || e).clipboardData || window.clipboardData).getData('Text');
        e.preventDefault();
        setTimeout(function () {
            document.execCommand('insertText', false, bufferText);
        }, 10);
    };

    $('#summernote').summernote({
        height: 300,
        focus: false,
        callbacks: {
            onPaste: handlePaste
        }
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
            },
            onPaste: handlePaste
        }
    });
})();