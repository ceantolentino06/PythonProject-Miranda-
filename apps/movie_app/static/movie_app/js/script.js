$(document).ready(function(){
    var POSTER_BASEURL = 'https://image.tmdb.org/t/p/w500';
    url = 'https://api.themoviedb.org/3/movie/now_playing?api_key=5d576382955ff5829fc3844390db4427&language=en-US&page=1&region=US'

    $.get(url, function(res){
        var results = res.results;
        var content = '';
                    // <div class="container col-lg-3 col-sm-4 mt-3">
                    //     <a href="/view"><img class="img-fluid border-dark"
                    //             src="{% static 'movie_app/images/sample.jpg' %}" alt="" /></a>
                    // </div>
        console.log(results)
        for(var i = 0; i<12; i++){
            var poster = POSTER_BASEURL+results[i].poster_path
            var movieID = results[i].id
            content += "<div class='container col-lg-3 col-sm-4 mt-3'>" +
                            "<a href='/"+ movieID +"/view'><img class='img-fluid' src="+ poster+"></a>"+
                        "</div>"
        }
        $('#showing').append(content)
    })
})

