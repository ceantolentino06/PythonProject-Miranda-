$(document).ready(function(){
    $('#search').click(function(){
        $('#results').empty();
        var title = $('#search_text').val()
        url = "https://api.themoviedb.org/3/search/movie?api_key=5d576382955ff5829fc3844390db4427&language=en-US&query="+ title +"&page=1&include_adult=false"
        $.get(url, function(res){
            var POSTER_BASEURL = 'https://image.tmdb.org/t/p/w500';
            var results = res.results;
            content = '';
            for(var i = 0; i<12; i++){
                var poster = POSTER_BASEURL+results[i].poster_path
                var movieID = results[i].id
                var title = results[i].title
                content += "<div class='container col-md-4 col-sm-4 col-xs-6 mt-3'>" +
                                "<a href='/"+ movieID +"/view'><img class='img-thumbnail' src="+ poster+"></a>"+
                                "<p>"+ title +"</p>"+
                            "</div>"
            }
            $('#results').append(content)
        })
    })
})