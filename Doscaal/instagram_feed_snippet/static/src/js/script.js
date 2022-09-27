odoo.define('instagram_feed_snippet.script', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var utils = require('web.utils');

    var qweb = core.qweb;
    var _t = core._t;
    var html = document.documentElement;
    var website_id = html.getAttribute('data-website-id') | 0;

    return ajax.jsonRpc("/get/instagram/credentials", 'call', { 'website_id': website_id}).then(function(data) {
        if (data.error) {
            console.log("Data error");
        } else {
            if ($("#instafeed").length && data.instagram_access_token) {
                if (data.instagram_feed_design == 'slider') {
                    $("#instafeed").addClass('owl-carousel owl-theme');
                    $(".load_more").addClass('d-none');
                    var size = 5;
                    if (data.instagram_row && Number.isSafeInteger(data.instagram_row) && data.instagram_row < 7 && data.instagram_row > 1) {
                        size = data.instagram_row;
                    }
                    if (data.user_picture) {
                        var user_picture = data.user_picture;
                    }

                    var feed = new Instafeed({
                        accessToken: data.instagram_access_token,
                        target: 'instafeed',
                        limit: 25,
                        after: function () {
                            var owl = $('#instafeed');
                            owl.owlCarousel({
                                autoplay: true,
                                autoplayTimeout: data.slider_speed,
                                loop: true,
                                margin: 15,
                                nav: true,
                                dots: false,
                                owl2row: 'true',
                                owl2rowTarget: 'item',
                                owl2rowContainer: 'owl2row-item',
                                owl2rowDirection: 'utd',
                                responsive: {
                                    0: {
                                        items: 1
                                    },
                                    600: {
                                        items: 2
                                    },
                                    800: {
                                        items: 3
                                    },
                                    1000: {
                                        items: data.instagram_row
                                    },
                                    1700: {
                                        items: 5
                                    },
                                    2000: {
                                        items: 6
                                    },
                                    3000: {
                                        items: 8
                                    },
                                    4000: {
                                        items: 10
                                    }
                                }
                            });
                        },
                        template: '<div class="item p-1" data-id="{{id}}"><div><div class="panel panel-default"><div class="panel-body card"><div class="user_profile"><div class="profile_picture"><img src="' + "data:image/;base64," + user_picture + '" alt="" class="rounded-circle"/></div><div class="profile"><div class="uname">{{username}}</div><div class="date_post">{{fulldate}}</div></div></div><div class=""></div><div class ="doc"><img data-toggle="modal" data-target="#masterModal" data-caption="{{caption}}" data-likes="{{model.likes.count}}" data-comments="{{model.comments.count}}" data-media_type="{{model.media_type}}" data-url="{{image}}" class="img-responsive show" src="{{image}}" data-video-url="{{model.media_url}}" class="img-responsive show" src="{{model.media_url}}" data-carousel="{{carousel_html}}" data-textval = "{{userheader}}" data-user-pic="' + "data:image/;base64," + user_picture + '" data-username="{{username}}" data-postdate="{{timestamp}}" data-view-instagram="{{link}}"/><span class="icon_set">{{iconset}}</span><div class="links"><i class="fa fa-heart"></i></div></div><div class="panel_body_text"><div class="body_text">{{caption}}</div></div></div></div></div></div>',
                    });
                    feed.run();
                } else {
                    $("#instafeed").removeClass('owl-carousel owl-theme');
                    $(".load_more").removeClass('d-none');
                    var size = 5;
                    var no_of_row = data.instagram_number_of_row

                    if (data.instagram_row && Number.isSafeInteger(data.instagram_row) && data.instagram_row < 7 && data.instagram_row > 1) {
                        size = data.instagram_row;
                    }
                    if (data.user_picture) {
                        var user_picture = data.user_picture;
                    }

                    var feed = new Instafeed({
                        accessToken: data.instagram_access_token,
                        target: 'instafeed',
                        template: '<div class="no_of_row_r'+ no_of_row +' ig_post x' + size +'" data-id="{{id}}"><div><div class="panel panel-default"><div class="panel-body card"><div class="user_profile"><div class="profile_picture"><img src="' + "data:image/;base64," + user_picture + '" alt="" class="rounded-circle"/></div><div class="profile"><div class="uname">{{username}}</div><div class="date_post">{{fulldate}}</div></div></div><div class=""></div><div class ="doc"><img data-toggle="modal" data-target="#masterModal" data-caption="{{caption}}" data-likes="{{model.likes.count}}" data-comments="{{model.comments.count}}" data-media_type="{{model.media_type}}" data-url="{{image}}" class="img-responsive show" src="{{image}}" data-video-url="{{model.media_url}}" class="img-responsive show" src="{{model.media_url}}" data-carousel="{{carousel_html}}" data-textval = "{{userheader}}" data-user-pic="' + "data:image/;base64," + user_picture + '" data-username="{{username}}" data-postdate="{{timestamp}}" data-view-instagram="{{link}}"/><span class="icon_set">{{iconset}}</span><div class="links"><i class="fa fa-heart"></i></div></div><div class="panel_body_text"><div class="body_text">{{caption}}</div></div></div></div></div></div>'
                    });
                    feed.run();
                }
            }
        }
        $('#instafeed').on("click", ".show", function() {
            $(this).closest("div.col-lg-2").addClass('active');
            $("#masterImg").html('<h2>Loading...</h2>');
            var mediaType = $(this).attr("data-media_type");
            if (mediaType == 'IMAGE'){
                var postData = $(this).attr("data-url");
                $("#masterImg").html('<img class="img-responsive card-img" src="' + postData + '" >');
            }
            else if (mediaType == 'VIDEO'){
                var video_url = $(this).attr("data-video-url");
                $("#masterImg").html('<div class="insta_video embed-responsive embed-responsive-16by9"><video autoplay muted loop controls><source src="' + video_url + '" type="video/mp4"/>');
            }
            else {
                var carousel = $(this).attr("data-carousel");
                $("#masterImg").html(carousel);

            }

            var caption = $(this).attr("data-caption");
            $("#masterCaption").text(caption);
            
            var postdate = $(this).attr("data-postdate");
            var fulldate = moment(postdate).format("DD.MM.YYYY HH:mm");
            var caption_model =$("#captiontest").html('<div class="likes_icon" id="fb_insta"><span id="Likes">Likes</span></div><div class="date_post" id="PostDate"></div><span class="icon"><i class="fa fa-instagram"></i></span>');
            $("#PostDate").text(fulldate);

            var likes = $(this).attr("data-likes") + ' likes';
            $("#Likes").text(likes);

            // var comments = $(this).attr("data-comments") + ' comments';
            // $("#Comments").text(comments);
            

            var user_pic = $(this).attr("data-user-pic");
            $("#UserImage").html('<img class="img-responsive" src="' + user_pic + '">');

            var username = '@' + $(this).attr("data-username");
            $("#Username").text(username);

            var postdate = $(this).attr("data-postdate");
            var fulldate = moment(postdate).format("DD.MM.YYYY HH:mm");
            $("#PostDate").text(fulldate);

            var viewlink = $(this).attr("data-view-instagram");
            $('#in_share').attr('href', viewlink);

            var fb_base = "https://www.facebook.com/sharer/sharer.php?u=";
            var fb_share = fb_base + encodeURIComponent(viewlink);
            $('#fb_share').attr('href', fb_share);

            var tw_base = "https://twitter.com/intent/tweet?url=";
            var tw_share = tw_base + encodeURIComponent(viewlink);
            $('#tw_share').attr('href', tw_share);
        });

        // $('.navigation').on("click", ".fa-angle-left", function() {
        //     var $current_el = $('#instafeed').find('div.active').removeClass('active');
        //     var new_el;
        //     if ($current_el.prev().length > 0) {
        //         var new_el = $current_el.prev().addClass('active');
        //     } else {
        //         var new_el = $('#instafeed').find('.ig_post').last().addClass('active');
        //     }
        //     update_model(new_el);
        // });

        // $('.navigation').on("click", ".fa-angle-right", function() {
        //     var $current_el = $('#instafeed').find('div.active').removeClass('active');
        //     var new_el;
        //     if ($current_el.next().length > 0) {
        //         var new_el = $current_el.next().addClass('active');
        //     } else {
        //         var new_el = $('#instafeed').find('.ig_post').first().addClass('active');
        //     }
        //     update_model(new_el);
        // });

        function update_model(new_el) {
            var $el = new_el.find('img');
            $("#masterImg").html('<h2>Loading...</h2>');

            var postData = $el.attr("data-url");
            $("#masterImg").html('<img class="img-responsive" src="' + postData + '"><div class="icon"><i class="fa fa-clone"/></div>');

            var caption = $el.attr("data-caption");
            $("#masterCaption").text(caption);
           
            
            $("#captiontest").html('<div class="likes_icon" id="fb_insta" ><span id="Likes">18 Likes</span><div class="post_date" id="PostDate">23.09.2021 11:16</div></div><span class="icon"><i class="fa fa-instagram"></i></span>');

            var captiontest = $(this).attr("data-caption-test");
            $("#captiontest").text(captiontest);
            
            var likes_icon = $(this).attr("data-caption-test");
            $("#likeicon").text(captiontest);

            var likes = $el.attr("data-likes") + ' likes';
            $("#Likes").text(likes);

            var comments = $el.attr("data-comments") + ' comments';
            $("#Comments").text(comments);

            var user_pic = $el.attr("data-user-pic");
            $("#UserImage").html('<img class="img-responsive" src="' + user_pic + '">');
            

            var username = '@' + $el.attr("data-username");
            $("#Username").text(username);

            // var postdate = $(this).attr("data-postdate");
            // var fulldate = moment(postdate).format("DD.MM.YYYY HH:mm");
            // $("#PostDate").text(fulldate);
            
            var text = $('#attrText'). $el.attr("data-textval");
            $(".attrText").text(text);s

            var viewlink = $el.attr("data-view-instagram");
            $('#in_share').attr('href', viewlink);


            var fb_insta = '<div class="captiontest"><span class="icon"><i class="fa fa-instagram"></i></div>';
            var fb_insta = fb_insta + encodeURIComponent(viewlink);
            $('#fb_insta').attr('href', fb_insta);

            var fb_base = "https://www.facebook.com/sharer/sharer.php?u=";
            var fb_share = fb_base + encodeURIComponent(viewlink);
            $('#fb_share').attr('href', fb_share);

            var tw_base = "https://twitter.com/intent/tweet?url=";
            var tw_share = tw_base + encodeURIComponent(viewlink);
            $('#tw_share').attr('href', tw_share);
        }
        $('#wrap').on("click", ".load_more", function() {
            var width = $(window).width();
                $('#instafeed > div').slideDown('slow');
                $('.load_more').hide();
        });

        $("#masterModal").keydown(function(e) {
            if (e.keyCode == 37) { // left
                $('.navigation').find('.fa-angle-left').trigger('click');
            } else if (e.keyCode == 39) { // right
                $('.navigation').find('.fa-angle-right').trigger('click');

            }
        });

        $('.o_main_navbar').on("click", "a[data-action=edit]", function() {
            $('#instafeed > div').remove();
        });

    });
});