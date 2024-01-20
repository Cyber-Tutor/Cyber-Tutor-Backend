// Dynamically load modules for a course
// 
$(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('course_id');

    if (courseId) {
        loadModules(courseId);
    }
});

function loadModules(courseId) {
    // This portion does not currently work anymore, but I will get to fixing it. If someone else wants to hop on it, feel free. All this is meant to do is highlight the course that is currently selected, like in the previous version of the site.
    $('#courseList a').removeClass('active');
    $(`#courseList a[data-course-id="${courseId}"]`).addClass('active');
    // End of portion that does not work

    const moduleDetails = $('#moduleDetails');
    moduleDetails.empty();

    $.ajax({
        url: `/courses/${courseId}/modules/`,
        type: 'GET',
        dataType: 'json',
        success: function (modules) {
            modules.forEach(function (module) {
                let cardHtml = `
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
            moduleDetails.html('<div class="alert alert-danger">Failed to load modules.</div>');
        }
    });
}
