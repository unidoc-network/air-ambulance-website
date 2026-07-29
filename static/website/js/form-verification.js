document.addEventListener('DOMContentLoaded', function () {
    // Select all forms: regional forms, contact main form, drawer form, and apply form
    const forms = document.querySelectorAll('.oman-main-form, .contact-main-form, .enquiry-form, .apply-form');

    forms.forEach(function (form) {
        const nameInput = form.querySelector('input[name="name"]');
        const servicesSelect = form.querySelector('select[name="services"]');
        const emailInput = form.querySelector('input[type="email"], input[name="email"]');
        const phoneInput = form.querySelector('input[type="tel"], input[name="phone"]');
        const locationInput = form.querySelector('input[name="location"]');
        const fileInput = form.querySelector('input[type="file"]');
        const verifyBtn = form.querySelector('.verify-email-btn');
        const codeInput = form.querySelector('input[name="verify_code"]');
        const messageTextarea = form.querySelector('textarea[name="message"]');
        const consentCheckbox = form.querySelector('input[type="checkbox"][name="consent"]');
        const submitBtn = form.querySelector('button[type="submit"], .oman-btn-submit, .btn-submit');
        
        let isEmailVerified = false;
        let otpTimeoutId = null;
        let formTimeoutId = null;

        // If this is the drawer form, set the country dynamically based on current page
        const countryInput = form.querySelector('#drawer-country');
        if (countryInput) {
            const path = window.location.pathname.toLowerCase();
            if (path.includes('oman')) {
                countryInput.value = 'Oman';
            } else if (path.includes('saudi')) {
                countryInput.value = 'Saudi Arabia';
            } else if (path.includes('qatar')) {
                countryInput.value = 'Qatar';
            } else if (path.includes('bahrain')) {
                countryInput.value = 'Bahrain';
            } else {
                countryInput.value = 'Website';
            }
        }

        // Initialize UI states
        if (codeInput) {
            codeInput.disabled = true;
            codeInput.style.backgroundColor = '#f1f5f9';
            codeInput.style.cursor = 'not-allowed';
        }

        // Keep submit button enabled so clicking it can show missing fields
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        }

        // 1. Create OTP verification specific status message (located below the verify email button)
        const otpStatusMsg = document.createElement('div');
        otpStatusMsg.className = 'otp-validation-status';
        otpStatusMsg.style.fontSize = '13px';
        otpStatusMsg.style.marginTop = '8px';
        otpStatusMsg.style.fontWeight = '600';
        otpStatusMsg.style.padding = '6px 10px';
        otpStatusMsg.style.borderRadius = '4px';
        otpStatusMsg.style.display = 'none';
        if (verifyBtn && verifyBtn.parentNode) {
            verifyBtn.parentNode.appendChild(otpStatusMsg);
        }

        // 2. Create general form submission status message (located above the submit button)
        const formStatusMsg = document.createElement('div');
        formStatusMsg.className = 'form-validation-status';
        formStatusMsg.style.fontSize = '14px';
        formStatusMsg.style.marginTop = '10px';
        formStatusMsg.style.marginBottom = '10px';
        formStatusMsg.style.fontWeight = '600';
        formStatusMsg.style.padding = '8px 12px';
        formStatusMsg.style.borderRadius = '6px';
        formStatusMsg.style.display = 'none';
        if (submitBtn && submitBtn.parentNode) {
            submitBtn.parentNode.insertBefore(formStatusMsg, submitBtn);
        }

        // Helper to update OTP Status Msg UI
        function showOTPAlert(msg, color) {
            if (otpTimeoutId) clearTimeout(otpTimeoutId);
            
            otpStatusMsg.innerText = msg;
            otpStatusMsg.style.color = color === 'red' ? '#991b1b' : (color === 'green' ? '#166534' : color);
            otpStatusMsg.style.backgroundColor = color === 'red' ? '#fee2e2' : (color === 'green' ? '#dcfce7' : '#e0f2fe');
            otpStatusMsg.style.borderColor = color === 'red' ? '#fca5a5' : (color === 'green' ? '#86efac' : '#bae6fd');
            otpStatusMsg.style.borderStyle = 'solid';
            otpStatusMsg.style.borderWidth = '1px';
            otpStatusMsg.style.display = 'block';

            // Auto-hide alert after 5 seconds if not loading
            if (!msg.includes('...') && !msg.toLowerCase().includes('sending') && !msg.toLowerCase().includes('verifying')) {
                otpTimeoutId = setTimeout(() => {
                    otpStatusMsg.style.display = 'none';
                }, 5000);
            }
        }

        // Helper to update Form Status Msg UI
        function showFormAlert(msg, color) {
            if (formTimeoutId) clearTimeout(formTimeoutId);

            formStatusMsg.innerText = msg;
            formStatusMsg.style.color = color === 'red' ? '#991b1b' : (color === 'green' ? '#166534' : color);
            formStatusMsg.style.backgroundColor = color === 'red' ? '#fee2e2' : (color === 'green' ? '#dcfce7' : '#e0f2fe');
            formStatusMsg.style.borderColor = color === 'red' ? '#fca5a5' : (color === 'green' ? '#86efac' : '#bae6fd');
            formStatusMsg.style.borderStyle = 'solid';
            formStatusMsg.style.borderWidth = '1px';
            formStatusMsg.style.display = 'block';

            // Auto-hide alert after 5 seconds if not loading
            if (!msg.includes('...') && !msg.toLowerCase().includes('submitting')) {
                formTimeoutId = setTimeout(() => {
                    formStatusMsg.style.display = 'none';
                }, 5000);
            }
        }

        const countryCodeSelect = form.querySelector('select[name="country_code"]');
        
        function updatePhoneMaxLength() {
            if (!phoneInput || !countryCodeSelect) return;
            const code = countryCodeSelect.value;
            let maxLength = 15; // default max length for "others"
            if (code === '+91') {
                maxLength = 10;
            } else if (code === '+971') {
                maxLength = 9;
            } else if (code === '+966') {
                maxLength = 9;
            } else if (['+965', '+968', '+974', '+973'].includes(code)) {
                maxLength = 8;
            }
            phoneInput.setAttribute('maxlength', maxLength);
        }

        if (countryCodeSelect && phoneInput) {
            countryCodeSelect.addEventListener('change', function() {
                updatePhoneMaxLength();
                // Trim phone if it exceeds new length
                const cleanPhone = phoneInput.value.replace(/[^0-9]/g, '');
                const maxLen = parseInt(phoneInput.getAttribute('maxlength') || '15', 10);
                if (cleanPhone.length > maxLen) {
                    phoneInput.value = cleanPhone.slice(0, maxLen);
                }
            });
            // Initial call
            updatePhoneMaxLength();
        }

        // Phone number input restriction: strictly restrict to digits and enforce length
        if (phoneInput) {
            phoneInput.addEventListener('input', function (e) {
                // Allow only digits to accurately measure length based on country code
                this.value = this.value.replace(/[^0-9]/g, '');
                
                const maxLen = parseInt(this.getAttribute('maxlength') || '15', 10);
                if (this.value.length > maxLen) {
                    this.value = this.value.slice(0, maxLen);
                }
            });
        }

        // Career file upload name update
        if (fileInput) {
            fileInput.addEventListener('change', function (e) {
                const fileLabel = form.querySelector('.file-label');
                if (fileLabel) {
                    if (this.files && this.files[0]) {
                        const fileName = this.files[0].name;
                        fileLabel.innerHTML = `<i class="fas fa-file-pdf" style="margin-right: 8px;"></i> ${fileName}`;
                    } else {
                        // Reset back to default bilingual translation spans
                        fileLabel.innerHTML = `
                            <span class="en-content">Attach resume/CV</span>
                            <span class="ar-content">إرفاق السيرة الذاتية</span>
                        `;
                    }
                }
            });
        }

        // OTP Input Validation: Restrict to digits only and max length 4
        if (codeInput) {
            codeInput.addEventListener('input', function (e) {
                let val = this.value.replace(/\D/g, '');
                if (val.length > 4) {
                    val = val.slice(0, 4);
                }
                this.value = val;

                // Auto-verify when exactly 4 digits are reached
                if (val.length === 4) {
                    verifyOTPCode(val);
                }
            });
        }

        // Trigger OTP Sending
        if (verifyBtn) {
            verifyBtn.addEventListener('click', function (e) {
                e.preventDefault();
                const email = emailInput ? emailInput.value.trim() : '';
                
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!email || !emailRegex.test(email)) {
                    showOTPAlert('Please enter a valid email address first.', 'red');
                    if (emailInput) emailInput.focus();
                    return;
                }

                // Disable verify button during send
                verifyBtn.disabled = true;
                verifyBtn.style.opacity = '0.7';
                verifyBtn.innerText = 'Sending OTP...';
                showOTPAlert('Sending verification code to your email...', '#009BE0');

                const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value;
                const formData = new FormData();
                formData.append('email', email);

                fetch('/send-otp/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                })
                .then(response => response.json().then(data => ({ status: response.status, body: data })))
                .then(res => {
                    if (res.status === 200) {
                        showOTPAlert('Verification code sent to your email. Check inbox / spam.', 'green');
                        verifyBtn.innerText = 'OTP Sent';
                        verifyBtn.style.backgroundColor = '#64748b';
                        verifyBtn.style.cursor = 'not-allowed';
                        
                        // Enable code input
                        if (codeInput) {
                            codeInput.disabled = false;
                            codeInput.style.backgroundColor = '#ffffff';
                            codeInput.style.cursor = 'text';
                            codeInput.focus();
                        }
                    } else {
                        // Reset button
                        verifyBtn.disabled = false;
                        verifyBtn.style.opacity = '1';
                        verifyBtn.innerText = 'Click here to verify your email';
                        showOTPAlert(res.body.message || 'Failed to send OTP. Please try again.', 'red');
                    }
                })
                .catch(error => {
                    verifyBtn.disabled = false;
                    verifyBtn.style.opacity = '1';
                    verifyBtn.innerText = 'Click here to verify your email';
                    showOTPAlert('An error occurred. Please try again.', 'red');
                    console.error('Send OTP Error:', error);
                });
            });
        }

        // Verify OTP Code
        function verifyOTPCode(otp) {
            const email = emailInput ? emailInput.value.trim() : '';
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value;
            
            showOTPAlert('Verifying code...', '#009BE0');
            codeInput.style.borderColor = '#cbd5e1';

            const formData = new FormData();
            formData.append('email', email);
            formData.append('otp', otp);

            fetch('/verify-otp/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(res => {
                if (res.status === 200) {
                    isEmailVerified = true;
                    showOTPAlert('Email verified successfully!', 'green');
                    
                    // Lock input fields
                    emailInput.readOnly = true;
                    emailInput.style.backgroundColor = '#f1f5f9';
                    codeInput.disabled = true;
                    codeInput.style.backgroundColor = '#f1f5f9';
                    codeInput.style.borderColor = 'green';
                    
                    // Add success badge next to email field
                    const emailGroup = emailInput.parentNode;
                    const successBadge = document.createElement('span');
                    successBadge.innerHTML = ' <i class="fas fa-check-circle" style="color: green;"></i> Verified';
                    successBadge.style.fontSize = '12px';
                    successBadge.style.color = 'green';
                    successBadge.style.fontWeight = 'bold';
                    successBadge.style.marginLeft = '8px';
                    
                    const label = emailGroup.querySelector('label');
                    if (label) {
                        label.appendChild(successBadge);
                    } else {
                        emailInput.parentNode.insertBefore(successBadge, emailInput.nextSibling);
                    }
                } else {
                    codeInput.style.borderColor = 'red';
                    showOTPAlert(res.body.message || 'Invalid code. Please try again.', 'red');
                }
            })
            .catch(error => {
                showOTPAlert('An error occurred during verification.', 'red');
                console.error('Verify OTP Error:', error);
            });
        }

        // Intercept Form Submit & Validate
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Clear any old form alerts
            formStatusMsg.style.display = 'none';
            if (formTimeoutId) clearTimeout(formTimeoutId);

            // 1. Validate Name
            if (nameInput && nameInput.value.trim().length < 2) {
                showFormAlert('Please enter your Name (at least 2 characters).', 'red');
                nameInput.style.borderColor = 'red';
                nameInput.focus();
                return;
            } else if (nameInput) {
                nameInput.style.borderColor = '';
            }

            // 2. Validate Service Selection
            if (servicesSelect && (!servicesSelect.value || servicesSelect.value === '')) {
                showFormAlert('Please choose a service from the dropdown.', 'red');
                servicesSelect.style.borderColor = 'red';
                servicesSelect.focus();
                return;
            } else if (servicesSelect) {
                servicesSelect.style.borderColor = '';
            }

            // 3. Validate Email Format
            const email = emailInput ? emailInput.value.trim() : '';
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!email || !emailRegex.test(email)) {
                showFormAlert('Please enter a valid Email Address.', 'red');
                if (emailInput) {
                    emailInput.style.borderColor = 'red';
                    emailInput.focus();
                }
                return;
            } else if (emailInput) {
                emailInput.style.borderColor = '';
            }

            // 4. Validate Email Verification Status
            if (!isEmailVerified) {
                if (codeInput && codeInput.disabled) {
                    showFormAlert('Please click the "Click here to verify your email" button to receive your OTP.', 'red');
                    if (verifyBtn) verifyBtn.focus();
                } else {
                    showFormAlert('Please enter the 4-digit code sent to your email to verify.', 'red');
                    if (codeInput) {
                        codeInput.style.borderColor = 'red';
                        codeInput.focus();
                    }
                }
                return;
            }

            // 5. Validate Phone
            const phone = phoneInput ? phoneInput.value.trim() : '';
            const cleanPhone = phone.replace(/[\s\-\(\)\+]/g, '');
            const countryCodeSelect = form.querySelector('select[name="country_code"]');
            const countryCode = countryCodeSelect ? countryCodeSelect.value : '';
            
            let isValidPhone = true;
            let phoneErrorMsg = '';

            if (!phone) {
                isValidPhone = false;
                phoneErrorMsg = 'Please enter your Phone Number.';
            } else if (countryCode === '+91' && cleanPhone.length !== 10) {
                isValidPhone = false;
                phoneErrorMsg = 'Please enter a valid 10-digit Indian phone number.';
            } else if (countryCode === '+971' && (cleanPhone.length < 8 || cleanPhone.length > 9)) {
                isValidPhone = false;
                phoneErrorMsg = 'Please enter a valid 8 or 9-digit UAE phone number.';
            } else if (countryCode === '+966' && cleanPhone.length !== 9) {
                isValidPhone = false;
                phoneErrorMsg = 'Please enter a valid 9-digit Saudi phone number.';
            } else if (['+965', '+968', '+974', '+973'].includes(countryCode) && cleanPhone.length !== 8) {
                isValidPhone = false;
                phoneErrorMsg = 'Please enter a valid 8-digit phone number for GCC.';
            } else if (!['+91', '+971', '+966', '+965', '+968', '+974', '+973'].includes(countryCode) && (cleanPhone.length < 7 || cleanPhone.length > 15)) {
                isValidPhone = false;
                phoneErrorMsg = 'Please enter a valid phone number (7 to 15 digits).';
            }

            if (!isValidPhone) {
                showFormAlert(phoneErrorMsg, 'red');
                if (phoneInput) {
                    phoneInput.style.borderColor = 'red';
                    phoneInput.focus();
                }
                return;
            } else if (phoneInput) {
                phoneInput.style.borderColor = '';
            }

            // 6. Validate Location (Careers form specific)
            if (locationInput && locationInput.value.trim().length < 2) {
                showFormAlert('Please enter your Location.', 'red');
                locationInput.style.borderColor = 'red';
                locationInput.focus();
                return;
            } else if (locationInput) {
                locationInput.style.borderColor = '';
            }

            // 7. Validate File Input (Careers resume upload)
            if (fileInput && fileInput.required && (!fileInput.files || !fileInput.files[0])) {
                showFormAlert('Please attach your Resume/CV.', 'red');
                fileInput.focus();
                return;
            }

            // 8. Validate Message
            if (messageTextarea && messageTextarea.value.trim().length < 10) {
                showFormAlert('Please enter your Message (at least 10 characters).', 'red');
                messageTextarea.style.borderColor = 'red';
                messageTextarea.focus();
                return;
            } else if (messageTextarea) {
                messageTextarea.style.borderColor = '';
            }

            // 9. Validate Consent Checkbox (Contact forms specific)
            if (consentCheckbox && !consentCheckbox.checked) {
                showFormAlert('You must declare consent by checking the store consent checkbox before submitting.', 'red');
                consentCheckbox.focus();
                return;
            }

            // If all validation passes, disable submit button and send details via AJAX.
            // Hide the status alert completely since the button displays "Submitting..."
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.7';
            const originalBtnText = submitBtn.innerText;
            submitBtn.innerText = 'Submitting...';

            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value;
            const formData = new FormData(form);

            fetch(form.action || '/submit-enquiry/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(res => {
                if (res.status === 200 && res.body.redirect_url) {
                    window.location.href = res.body.redirect_url;
                } else {
                    submitBtn.disabled = false;
                    submitBtn.style.opacity = '1';
                    submitBtn.innerText = originalBtnText;
                    showFormAlert(res.body.message || 'Failed to submit. Please try again.', 'red');
                }
            })
            .catch(error => {
                submitBtn.disabled = false;
                submitBtn.style.opacity = '1';
                submitBtn.innerText = originalBtnText;
                showFormAlert('An error occurred during submission. Please try again.', 'red');
                console.error('Submission Error:', error);
            });
        });
    });
});
