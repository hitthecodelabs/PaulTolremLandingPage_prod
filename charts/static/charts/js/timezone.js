let timezoneOffset;

function fetchTimezoneOffset() {
    var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    var offsetInMinutes = moment().tz(timezone).utcOffset();
    var offsetInMilliseconds = offsetInMinutes * 60 * 1000;
    return offsetInMilliseconds;
}