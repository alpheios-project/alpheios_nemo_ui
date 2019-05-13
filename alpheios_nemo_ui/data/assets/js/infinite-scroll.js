var nextPassage = {};
var isloading = false;
var isInit = false;
var uploadOneMore = false;
var uploadOnemoreCheck  = null;

function preloadNext() {
    if ($('#next-passage').prop('href') === 'javascript:void(0)') {
        nextPassage = {}
        return
    }
    if (!nextPassage.nextUrl) {
        nextPassage.nextUrl = $('#next-passage').prop('href')
    }
    if ($('#current-passage').length > 0) {
        var deferred = $.Deferred();

        let currentSubrefData = $('#current-passage').data();

        if (!nextPassage.start) {
            nextPassage.start = currentSubrefData.subreference.toString().split('-')[0]
        }
        isloading = true

        $.getJSON(`${nextPassage.nextUrl}/json`)
            .done(function(data) {
                var finalRef = nextPassage.start
                var subRef = data.subreference.toString().split('-')
                if (subRef) {
                    finalRef = finalRef + '-' + subRef[subRef.length-1]
                }
                Object.assign(nextPassage, {
                    data: data,
                    next: data.next,
                    subreference: data.subreference.toString(),
                    finalRef: finalRef,
                    nextUrl: data.nextUrl
                })
                
                console.log('Retrieved next data', data.subreference.toString())
                isloading = false
                deferred.resolve(nextPassage);
            })
            .fail(function(error) {
              console.log( "error" , error);
            });

        return deferred.promise();
    }
}

function uploadNext() {
    if (nextPassage && nextPassage.data) {
        if (nextPassage.data.new_level) {
            $('#article-entry').append(`<div class="newlevel">${nextPassage.data.new_level}</div>`)
        }

        $('#article-entry').append(nextPassage.data.text_passage);
        $('#current-passage').data('subreference', nextPassage.next);     
        $('#current-passage').text(nextPassage.finalRef);

        if (nextPassage.data.next) {
            $('#next-passage').prop('data-next', nextPassage.data.next);
            $('#next-passage').prop('href', nextPassage.data.nextUrl);
        } else {
            $('#next-passage').prop('data-next', nextPassage.data.next);
            $('#next-passage').prop('href', 'javascript:void(0)');
            $('#next-passage').addClass('no-visibility');
        }
        if (!isInit) {
            preloadNext();
        }
    }
}

function initPassages() {
    if ($(window).scrollTop() + window.innerHeight + 10 > $(document).height()) {
        preloadNext()
        .done(function(){
            uploadNext();
            if ($(window).scrollTop() + window.innerHeight + 10 > $(document).height()) {
                initPassages();
            } else {
                isInit = false;
                preloadNext();
            }
        })
        
    } else {
        isInit = false;
        preloadNext();
    }
}

$(document).ready(function() {
    if ($('#current-passage').length > 0) {
        isInit = true;
        setTimeout(initPassages, 1000)

        $(window).scroll(function() {
            uploadOneMore = false;
            clearTimeout(uploadOnemoreCheck);

            if ($(window).scrollTop() + window.innerHeight + 10 >= $(document).height() && !isloading) {
                uploadNext();
            } else {
                uploadOneMore = true;
                uploadOnemoreCheck = setTimeout(function () {
                    if (uploadOneMore && !isloading) {
                        uploadNext();
                    }
                }, 1000);
            }
        });
    }
});