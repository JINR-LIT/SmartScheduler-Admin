jQuery(document).ready(function() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function showPopupMessage(content) {
        var elMessages = $('#popup-messages-content');
        if (elMessages.length && content) {
            elMessages.append(content);
        }
    }

    $("#load-cloud-conf").click(function() {
      location.href = '/load_cloud_conf';
    });

    $("#drop-cloud-conf").click(function() {
      location.href = '/drop_cloud_conf';
    });

    $("#id_admin_sync_host").click(function() {
      $("#sync_host_spinner").addClass("fa-spin");
      $.ajax({
          type: "POST",
          url: "/admin/get_host_info/",
          data: { host_id : $("#id_host_id").val()},
          success: function(json) {
              showPopupMessage(json.msg)
              $('#id_cluster').val(json.data.cluster_id);
              $('#id_cpu').val(json.data.cpu);
              $('#id_ram').val(json.data.ram);
              $("#sync_host_spinner").removeClass("fa-spin");
          },
          error: function(xhr, errmsg, err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
              $("#sync_host_spinner").removeClass("fa-spin");
          }
      });
    });

    $("#id_admin_sync_cluster").click(function() {
      $("#sync_cluster_spinner").addClass("fa-spin");
      $.ajax({
          type: "POST",
          url: "/admin/get_cluster_info/",
          data: { cluster_id : $("#id_cluster_id").val()},
          success: function(json) {
              showPopupMessage(json.msg)
              $('#id_cluster_name').val(json.data.name);
              $("#sync_cluster_spinner").removeClass("fa-spin");
          },
          error: function(xhr, errmsg, err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
              $("#sync_cluster_spinner").removeClass("fa-spin");
          }
      });
    });

    $("#id_admin_sync_vm").click(function() {
      $("#sync_vm_spinner").addClass("fa-spin");
      $.ajax({
          type: "POST",
          url: "/admin/get_vm_info/",
          data: { vm_id : $("#id_vm_id").val()},
          success: function(json) {
              showPopupMessage(json.msg)
              $('#id_cpu').val(json.data.cpu);
              $('#id_ram').val(json.data.ram);
              $("#id_host option:contains(" + json.data.host + ")").attr('selected', 'selected');
              $("#sync_vm_spinner").removeClass("fa-spin");
          },
          error: function(xhr, errmsg, err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
              $("#sync_vm_spinner").removeClass("fa-spin");
          }
      });
    });

    function draw_datetimepickers(date_from, date_to, active_modal) {
        $('#metrics_from').datetimepicker({date: new Date(date_from)}).on('show.bs.collapse', function(e){ e.stopPropagation() })
                                            .on('hidden.bs.collapse', function(e) {e.stopPropagation()});
        $('#metrics_to').datetimepicker({
            useCurrent: false,
            date: new Date(date_to)
        }).on('show.bs.collapse',function(e){ e.stopPropagation() })
          .on('hidden.bs.collapse', function(e) {e.stopPropagation()});


        $("#metrics_from").on("dp.change", function (e) {
            $('#metrics_to').data("DateTimePicker").minDate(e.date);
        });
        $("#metrics_to").on("dp.change", function (e) {
            $('#metrics_from').data("DateTimePicker").maxDate(e.date);
        });

        $("#update_metrics").click(function(){
          date_from = $('#metrics_from').data('DateTimePicker').date();
          date_to = $('#metrics_to').data('DateTimePicker').date();

          if (active_modal === undefined){
            $("#performance_metrics").find("iframe").each(function (index) {
              var src = $( this ).attr('src');
              var newSrc = src.replace(/(to=).*?(&)/,'$1' + date_to + '$2').replace(/(from=).*?(&)/,'$1' + date_from + '$2');
              $( this ).attr('src', newSrc);
            });
          } else {
            active_modal.find("iframe").each(function (index) {
              var src = $( this ).attr('src');
              var newSrc = src.replace(/(to=).*?(&)/,'$1' + date_to + '$2').replace(/(from=).*?(&)/,'$1' + date_from + '$2');
              $( this ).attr('src', newSrc);
            });
          }
        });
    }

    $("#host_performance_metrics").on('show.bs.collapse', function(){
      $("#host_perf_body").html('<i class="fa fa-spinner fa-pulse fa-3x" id="metrics_spinner" aria-hidden="True" style="margin:auto;"></i>');
      $.ajax({
          type: "POST",
          url: "/admin/get_host_metrics/",
          data: { host_id : $("#id_host_id").val()},
          success: function(json) {
              $("#host_perf_body").html(json.data.html);
              draw_datetimepickers(parseInt(json.data.date_from), parseInt(json.data.date_to));
          },
          error: function(xhr, errmsg, err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
    });

    $("#host_performance_metrics").on('hidden.bs.collapse', function(){
      $("#host_perf_body").html("");
    });

    $("#vm_performance_metrics").on('show.bs.collapse', function(){
      $("#vm_perf_body").html('<i class="fa fa-spinner fa-pulse fa-3x" id="metrics_spinner" aria-hidden="True" style="margin:auto;"></i>');
      $.ajax({
          type: "POST",
          url: "/admin/get_vm_metrics/",
          data: { vm_id : $("#id_vm_id").val()},
          success: function(json) {
              $("#vm_perf_body").html(json.data.html);
              draw_datetimepickers(parseInt(json.data.date_from), parseInt(json.data.date_to));
          },
          error: function(xhr, errmsg, err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
    });

    $("#vm_performance_metrics").on('hidden.bs.collapse', function(){
      $("#vm_perf_body").html("");
    });

    $("[id^=host_metrics]").on('shown.bs.modal', function(){
      var active_modal = $(this);
      $(this).find("#host_perf_body").html('<i class="fa fa-spinner fa-pulse fa-3x" id="metrics_spinner" aria-hidden="True" style="margin:auto;"></i>');

      $.ajax({
          type: "POST",
          url: "/admin/get_host_metrics/",
          data: { host_id : $.trim(active_modal.find("#modal_host_id").text())},
          success: function(json) {
              active_modal.find("#host_perf_body").html(json.data.html);
              draw_datetimepickers(parseInt(json.data.date_from), parseInt(json.data.date_to), active_modal);
          },
          error: function(xhr, errmsg, err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
    });

    $("[id^=host_metrics]").on('hidden.bs.modal', function(){
      $(this).find("#host_perf_body").html("");
    });

    $("[id^=vm_metrics]").on('shown.bs.modal', function(){
      var active_modal = $(this);
      $(this).find("#vm_perf_body").html('<i class="fa fa-spinner fa-pulse fa-3x" id="metrics_spinner" aria-hidden="True" style="margin:auto;"></i>');

      $.ajax({
          type: "POST",
          url: "/admin/get_vm_metrics/",
          data: { vm_id : $.trim(active_modal.find("#modal_vm_id").text())},
          success: function(json) {
              active_modal.find("#vm_perf_body").html(json.data.html);
              draw_datetimepickers(parseInt(json.data.date_from), parseInt(json.data.date_to), active_modal);
          },
          error: function(xhr, errmsg, err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
    });

    $("[id^=vm_metrics]").on('hidden.bs.modal', function(){
      $(this).find("#vm_perf_body").html("");
    });
});
