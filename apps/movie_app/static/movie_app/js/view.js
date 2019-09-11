$(document).ready(function () {
    $('#showtimes-container').hide()
    $('#buy').hide()
    $('#cinemas').click(function(){
        $('#showtimes-container').slideToggle()
        $('#arrow').toggleClass('fas fa-caret-right fas fa-caret-down')
    })
    $('#buy-text').click(function(){
        $('#buy').slideToggle()
        $('#arrow-buy').toggleClass('fas fa-caret-right fas fa-caret-down')
    })
    if (document.getElementById('reviewbtn')) {
        var modal = document.getElementById('rating-modal')
        var modalBtn = document.getElementById('reviewbtn')
        var closeBtn = document.getElementById('closebtn')

        modalBtn.addEventListener('click', openModal)

        closeBtn.addEventListener('click', closeModal)

        window.addEventListener('click', clickOutside)

        function openModal() {
            modal.style.display = 'flex'
        }

        function closeModal() {
            modal.style.display = 'none'
        }

        function clickOutside(e) {
            if (e.target == modal) {
                modal.style.display = 'none'
            }
        }
    }
    const apiRating = (Number($('#rating').val()) * Number($('#vote_count').val())) + Number($('#user_reviews').val())
    console.log($('#vote_count').val())
    const newTotalVote = Number($('#vote_count').val()) + Number($('#user_count').val())
    const rating = apiRating / newTotalVote
    console.log(newTotalVote)
    const starsTotal = 10;
    const starPercentage = (rating / starsTotal) * 100
    const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;
    console.log(starPercentageRounded)
    document.querySelector('.stars-inner').style.width = starPercentageRounded;

    console.log($('#user_count').val())
    var data = $("#rateForm").serialize()   // capture all the data in the form in the variable data
    $.ajax({
        method: "POST",   // we are using a post request here, but this could also be done with a get
        url: "/rate",
        data: data
    })
        .done(function (res) {
            $('#rateMsg').html(res)  // manipulate the dom when the response comes back
        })
    $('.rating').click(function () {
        var data = $("#rateForm").serialize()   // capture all the data in the form in the variable data
        $.ajax({
            method: "POST",   // we are using a post request here, but this could also be done with a get
            url: "/rate",
            data: data
        })
            .done(function (res) {
                $('#rateMsg').html(res)  // manipulate the dom when the response comes back
            })
    })

    
});