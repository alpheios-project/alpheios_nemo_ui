var nextPassage = {};
var isloading = false;
var isInit = false;
var uploadOneMore = false;
var uploadOnemoreCheck  = null;

function preloadNext() {
    if ($('#current-passage').length > 0) {
        var deferred = $.Deferred();

        let currentSubrefData = $('#current-passage').data();
        if (!nextPassage.start) {
            nextPassage.start = currentSubrefData.subreference.split('-')[0]
        }
        isloading = true
        $.getJSON( `/nextpassage/${currentSubrefData.objectid}/${currentSubrefData.subreference}`)
          .done(function( urlData ) {
            deferred.notify(urlData)

            $.getJSON(`${urlData.url}/json`)
            .done(function(data) {
                let nextArr = urlData.next.split('-');
                Object.assign(nextPassage, {
                    data: data,
                    next: urlData.next,
                    subreference: currentSubrefData.subreference,
                    finalRef: nextPassage.start + '-' + nextArr[nextArr.length-1],
                    nextRefUrl: urlData.nextRefUrl
                })
                
                console.log('Retrieved next data', urlData.url)
                isloading = false
                deferred.resolve(nextPassage);
            })
            .fail(function(error) {
              console.log( "error" , error);
            });
          })
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

        $('#next-passage').data('prev', nextPassage.data.next);
        $('#next-passage').prop('href', nextPassage.data.next);
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