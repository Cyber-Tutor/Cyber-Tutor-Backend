// course_list.html
function loadModules(courseId) {

  $('#courseList a').removeClass('active');
  $(`#courseList a[data-course-id="${courseId}"]`).addClass('active');
  
  $.ajax({
    url: `/courses/${courseId}/modules/`,
    type: 'GET',
    dataType: 'json',
    success: function (modules) {
      var moduleDetails = $('#moduleDetails');
      moduleDetails.empty();

      modules.forEach(function (module) {
        var cardHtml = `
            <a href="/courses/${courseId}/module/${module.id}" class="card-link">
              <div class="card mb-3 module-card">
                <div class="card-body">
                  <h5 class="card-title text-center">${module.title}</h5>
                  <p class="card-text">${module.description}</p>
                </div>
              </div>
            </a>`;
        moduleDetails.append(cardHtml);
      });
    },
    error: function () {
      $('#moduleDetails').html('<div class="alert alert-danger">Failed to load modules.</div>');
    }
  });
}

// module_detail.html
$(document).ready(function() {
  var moduleDetails = $('#moduleDetails');
  if (moduleDetails.length) {
    var courseId = moduleDetails.data('course-id');
    loadModulesForDetail(courseId);
  }
});

function loadModulesForDetail(courseId) {
  $.ajax({
    url: `/courses/${courseId}/modules/`,
    type: 'GET',
    dataType: 'json',
    success: function (modules) {
      var moduleDetails = $('#moduleDetails');
      moduleDetails.empty();

      modules.forEach(function (module) {
        // Change this HTML to fit how you want to display the modules in detail
        var listItemHtml = `
            <a href="/courses/${courseId}/module/${module.id}" class="list-group-item list-group-item-action">
              ${module.title}
            </a>`;
        moduleDetails.append(listItemHtml);
      });
    },
    error: function () {
      moduleDetails.html('<div class="alert alert-danger">Failed to load modules.</div>');
    }
  });
}

