const drop_area = document.getElementById('file-drop-area');
const file_input = document.getElementById('file-input');
const file_list = document.getElementById('file-list');

const submit = document.getElementById('submit');
const validate_empty_enable = document.querySelectorAll('.validate-empty');
const validate_select_enable = document.querySelectorAll('.validate-select');
const validate_checkbox_enable = document.querySelectorAll('.validate-checkbox');

const validate_notice = (validate_flag, target_id) => {
	const validate_notice = document.getElementById(target_id);
	validate_notice.classList.remove('fas', 'fa-check', 'has-text-success', 'fa-times', 'has-text-danger');
	if (validate_flag === true) {
		validate_notice.classList.add('fas', 'fa-check', 'has-text-success');
	} else {
		validate_notice.classList.add('fas', 'fa-times', 'has-text-danger');
		submit.setAttribute('disabled', true);
	}
}

const validate_form_data = () => {

	const accept = document.getElementById('accept');
	const form = document.getElementById('application-form');
	const form_data = new FormData(form);

	for (const item of form_data.entries()) {

		if (item[1] === '') {
			submit.setAttribute('disabled', true);
			break;
		}

		if (accept.checked === true) {
			submit.removeAttribute('disabled');
		} else {
			submit.setAttribute('disabled', true);
		}
	}
}

for (const validate_form of validate_empty_enable) {
	validate_form.addEventListener('change', (e) => {
		const validate = v8n().not.empty().test(e.target.value);
		const target_id = e.target.getAttribute('data-validate');
		console.log(target_id)
		validate_notice(validate, target_id);
		validate_form_data();
	});
};

for (const validate_form of validate_select_enable) {
	validate_form.addEventListener('change', (e) => {
		const index = e.target.selectedIndex;
		const value = e.target.options[index].value;
		const validate = v8n().not.empty().test(value);
		const target_id = e.target.getAttribute('data-validate');
		validate_form_data();
		validate_notice(validate, target_id);
	});
};

for (const validate_form of validate_checkbox_enable) {
	validate_form.addEventListener('change', (e) => {
		validate_form_data();
	});
};

document.body.addEventListener('click', (e) => {

	if (e.target.className.toLowerCase() === 'file-reset') {
		file_input.value = '';
		file_list.innerHTML = '';
	}
});

const add_file_name = (file_name) => {

	let html = '<span class="tag is-info m-1">';
	html += '<span class="cancel-upload">' + file_name + '</span><span>';
	file_list.insertAdjacentHTML('beforeend', html);
}

const add_file_reset_button = () => {

	let html = '<span class="button is-danger is-outlined is-small">';
	html += '<span class="file-reset">取消</span>';
	html += '<span class="icon is-small"><i class="fas fa-times"></i></span>';
	html += '</span></span>';

	file_list.insertAdjacentHTML('beforeend', html);
}

drop_area.addEventListener('dragover', (e) => {
	e.preventDefault();
});

drop_area.addEventListener('dragleave', (e) => {
	e.preventDefault();
});

drop_area.addEventListener('drop', (e) => {
	e.preventDefault();
	console.log('Drop event triggered');
	file_list.innerHTML = '';
	file_input.files = e.dataTransfer.files;
	let files = file_input.files;
	for (const file of files) {
		if (file.name.match(/\.(jpe?g|png|pdf)$/g)) {
			add_file_name(file.name);
		} else {
			console.log('err');
		}
	}
	add_file_reset_button();
});

file_input.addEventListener('change', (e) => {

	file_list.innerHTML = '';
	const files = e.target.files;
	for (const file of files) {
		add_file_name(file.name);
	}
	add_file_reset_button();

});