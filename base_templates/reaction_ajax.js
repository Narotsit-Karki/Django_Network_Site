
{% load static %}
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
        <script type="text/javascript">

        $('#like_reaction').click(function(){
            var slug = $(this).attr("post-id");
            $.ajax(
            {
                type:"POST",
                url: "/posts/like-unlike-post",
                data:{
                    post_slug: slug,
                    reaction: 'like',
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },

                success: function( data )
                {
                    if ( data.reacted == true){
                        $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/like.gif' %}");
                        }

                        else{
                            $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/like_outline.png' %}");
                        }
                    $( '#reaction-count' ).text(data.total_reactions);
                }
            })
        });


        $('#love_reaction').click(function(){
            var slug = $(this).attr("post-id");
            $.ajax(
            {
                type:"POST",
                url: "/posts/like-unlike-post",
                data:{
                    post_slug: slug,
                    reaction: 'love',
                    'csrfmiddlewaretoken': '{{ csrf_token }}',
                },

                success: function( data )
                {
                    if ( data.reacted == true){
                        $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/love.gif' %}");
                        }

                        else{
                            $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/like_outline.png' %}");
                        }
                    $( '#reaction-count' ).text(data.total_reactions);
                }
            })
        });
        $('#haha_reaction').click(function(){
            var slug = $(this).attr("post-id");
            $.ajax(
            {
                type:"POST",
                url: "/posts/like-unlike-post",
                data:{
                    post_slug: slug,
                    reaction: 'haha',
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },

                success: function( data )
                {
                    if ( data.reacted == true){
                        $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/haha.gif' %}");
                        }

                        else{
                            $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/like_outline.png' %}");
                        }
                    $( '#reaction-count' ).text(data.total_reactions);
                }
            })
        });

        $('#sad_reaction').click(function(){
            var slug = $(this).attr("post-id");
            $.ajax(
            {
                type:"POST",
                url: "/posts/like-unlike-post",
                data:{
                    post_slug: slug,
                    reaction: 'sad',
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },

                success: function( data )
                {
                    if ( data.reacted == true){
                        $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/sad.gif' %}");
                        }

                        else{
                            $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/like_outline.png' %}");
                        }
                    $( '#reaction-count' ).text(data.total_reactions);
                }
            })
        });

        $('#wow_reaction').click(function(){
            var slug = $(this).attr("post-id");
            $.ajax(
            {
                type:"POST",
                url: "/posts/like-unlike-post",
                data:{
                    post_slug: slug,
                    reaction: 'wow',
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },

                success: function( data )
                {
                    if ( data.reacted == true){
                        $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/wow.gif' %}");
                        }

                        else{
                            $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/like_outline.png' %}");
                        }
                    $( '#reaction-count' ).text(data.total_reactions);
                }
            })
        });

        $('#angry_reaction').click(function(){
            var slug = $(this).attr("post-id");
            $.ajax(
            {
                type:"POST",
                url: "/posts/like-unlike-post",
                data:{
                    post_slug: slug,
                    reaction: 'angry',
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },

                success: function( data )
                {
                    if ( data.reacted == true){
                        $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/angry.gif' %}");
                        }

                        else{
                            $( '#reaction-img' ).attr("src","{% static 'assets/images/icons/reactions/like_outline.png' %}");
                        }
                    $( '#reaction-count' ).text(data.total_reactions);
                }
            })
        });
    </script>