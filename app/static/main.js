const countDown = el => {
    let end = moment(el.dataset.timestamp)
    let now, diff, duration
    const timeinterval = setInterval(() => {
        now = moment()
        diff = end.diff(now)
        if (diff <= 0) {
            el.textContent = "0d:0h:0m:0s"
            clearTimeout(timeinterval)
        } else {
            duration = moment.duration(diff)
            el.textContent = `${duration.days()}d:${duration.hours()}h:${duration.minutes()}m:${duration.seconds()}s`
        }
    }, 100)
}

const date = () => {
    document.querySelectorAll("[data-date]").forEach(el => {
        if (el.dataset.date) {
            const d = new Date(el.dataset.date + 'Z')
            el.textContent = d.toLocaleString()
        }
    })
}

const bank = () => {
    const accountNoEl = document.querySelector("#account_no")
    const accountNameEl = document.querySelector("#account_name")
    const bankNameEl = document.querySelector("#bank")
    const submitBtn = document.querySelector('[type=submit]')
    accountNameEl.readOnly = true

    const fetchAccountDetails = () => {
        submitBtn.disabled = true
        let prevAccountName = accountNameEl.value
        accountNameEl.value = 'Fetching Details...'
        fetch("/account_no_verification", {
            method: 'POST',
            body: JSON.stringify({ account_no: accountNoEl.value, bank: bankNameEl.value })
        })
            .then(r => r.json())
            .then(({ account_name }) => accountNameEl.value = account_name)
            .catch(err => {
                accountNameEl.value = prevAccountName
                accountNameEl.readOnly = false
            })
            .finally(() => submitBtn.disabled = false)
    }

    accountNoEl.oninput = e => {
        if (accountNoEl.value.length == 10) {
            fetchAccountDetails()
        }
    }
    bankNameEl.oninput = e => {
        if (accountNoEl.value.length == 10) {
            fetchAccountDetails()
        }
    }
}

const onload = () => {
    fetch("/settimezone", {
        method: 'POST',
        body: JSON.stringify({ timezone: (new Date()).getTimezoneOffset() })
    })
    document.querySelectorAll(".countdown").forEach(countDown)
    
    document.querySelectorAll('[data-fileUpload]').forEach(el => {
        el.querySelector('input').onchange = uploadFile(el.querySelector('label'), el.dataset.fileupload)
    })
    date()
    bank()   
}

window.onload = onload

const open = () => (
    {
        'menuOpen': false, 'isOpen': false
    }
)


function focusTrap(element) {
    const focusableElements = getFocusableElements(element)
    const firstFocusableEl = focusableElements[0]
    const lastFocusableEl = focusableElements[focusableElements.length - 1]

    // Wait for the case the element was not yet rendered
    setTimeout(() => firstFocusableEl.focus(), 50)

    /**
     * Get all focusable elements inside `element`
     * @param {HTMLElement} element - DOM element to focus trap inside
     * @return {HTMLElement[]} List of focusable elements
     */
    function getFocusableElements(element = document) {
        return [
            ...element.querySelectorAll(
                'a, button, details, input, select, textarea, [tabindex]:not([tabindex="-1"])'
            ),
        ].filter((e) => !e.hasAttribute('disabled'))
    }

    function handleKeyDown(e) {
        const TAB = 9
        const isTab = e.key.toLowerCase() === 'tab' || e.keyCode === TAB

        if (!isTab) return

        if (e.shiftKey) {
            if (document.activeElement === firstFocusableEl) {
                lastFocusableEl.focus()
                e.preventDefault()
            }
        } else {
            if (document.activeElement === lastFocusableEl) {
                firstFocusableEl.focus()
                e.preventDefault()
            }
        }
    }

    element.addEventListener('keydown', handleKeyDown)

    return function cleanup() {
        element.removeEventListener('keydown', handleKeyDown)
    }
}

function data() {
    function getThemeFromLocalStorage() {
        // if user already changed the theme, use it
        if (window.localStorage.getItem('dark')) {
            return JSON.parse(window.localStorage.getItem('dark'))
        }

        // else return their preferences
        return (
            !!window.matchMedia &&
            window.matchMedia('(prefers-color-scheme: dark)').matches
        )
    }

    function setThemeToLocalStorage(value) {
        window.localStorage.setItem('dark', value)
    }

    return {
        mobileNavIsOpen: false, 
        isSideMenuOpen: false,
        toggleSideMenu() {
            this.isSideMenuOpen = !this.isSideMenuOpen
        },
        closeSideMenu() {
            this.isSideMenuOpen = false
        },
        isNotificationsMenuOpen: false,
        toggleNotificationsMenu() {
            this.isNotificationsMenuOpen = !this.isNotificationsMenuOpen
        },
        closeNotificationsMenu() {
            this.isNotificationsMenuOpen = false
        },
        isProfileMenuOpen: false,
        toggleProfileMenu() {
            this.isProfileMenuOpen = !this.isProfileMenuOpen
        },
        closeProfileMenu() {
            this.isProfileMenuOpen = false
        },
        isPagesMenuOpen: false,
        togglePagesMenu() {
            this.isPagesMenuOpen = !this.isPagesMenuOpen
        },
        // Modal
        isModalOpen: true,
        trapCleanup: null,
        openModal() {
            this.isModalOpen = true
            this.trapCleanup = focusTrap(document.querySelector('#modal'))
        },
        closeModal() {
            this.isModalOpen = false
            this.trapCleanup()
        },
    }
}


const uploadFile = (inputLbl, uploadUrl) => e => {
    console.log(uploadUrl)
    const sendToServer = url => {
        console.log(url)    
        fetch(uploadUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        })
            .then(r => {
                window.location.reload()
            })
    }
    const URL = 'https://api.cloudinary.com/v1_1/dnpxiezya/upload'
    const UPLOAD_PRESET = 'rafsjzaw'
    const file = e.target.files[0]

    const formData = new FormData()
    formData.append('file', file)
    formData.append('upload_preset', UPLOAD_PRESET)

    inputLbl.textContent = "Uploading..."

    fetch(URL, {
        method: 'POST',
        body: formData,
    })
        .then(r => r.json())
        .then(r => r.secure_url)
        .then(sendToServer)
        .catch(err => {
            inputLbl.textContent = "An Error Occured"
            console.log(err)
        })

}
