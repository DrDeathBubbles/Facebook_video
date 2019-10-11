# -*- coding: utf-8 -*-

html_email = """
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->

    <!-- Web Font / @font-face : BEGIN -->
    <!-- NOTE: If web fonts are not required, lines 10 - 27 can be safely removed. -->

    <!-- Desktop Outlook chokes on web font references and defaults to Times New Roman, so we force a safe fallback font. -->
    <!--[if mso]>
        <style>
            * {
                font-family: sans-serif !important;
            }
        </style>
    <![endif]-->

    <!-- All other clients get the webfont reference; some will render the font and others will silently fail to the fallbacks. More on that here: http://stylecampaign.com/blog/2015/02/webfont-support-in-email/ -->
    <!--[if !mso]><!-->
    <!-- insert web font reference, eg: <link href='https://fonts.googleapis.com/css?family=Roboto:400,700' rel='stylesheet' type='text/css'> -->
    <!--<![endif]-->

    <!-- Web Font / @font-face : END -->

    <!-- CSS Reset : BEGIN -->
    <style>

        /* What it does: Remove spaces around the email design added by some email clients. */
        /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */
        html,
        body {
            margin: 0 auto !important;
            padding: 0 !important;
            height: 100% !important;
            width: 100% !important;
        }

        /* What it does: Stops email clients resizing small text. */
        * {
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%;
        }

        /* What it does: Centers email on Android 4.4 */
        div[style*="margin: 16px 0"] {
            margin: 0 !important;
        }

        /* What it does: Stops Outlook from adding extra spacing to tables. */
        table,
        td {
            mso-table-lspace: 0pt !important;
            mso-table-rspace: 0pt !important;
        }

        /* What it does: Fixes webkit padding issue. Fix for Yahoo mail table alignment bug. Applies table-layout to the first 2 tables then removes for anything nested deeper. */
        table {
            border-spacing: 0 !important;
            border-collapse: collapse !important;
            table-layout: fixed !important;
            margin: 0 auto !important;
        }
        table table table {
            table-layout: auto;
        }

        /* What it does: Uses a better rendering method when resizing images in IE. */
        img {
            -ms-interpolation-mode:bicubic;
        }

        /* What it does: A work-around for email clients meddling in triggered links. */
        *[x-apple-data-detectors],  /* iOS */
        .unstyle-auto-detected-links *,
        .aBn {
            border-bottom: 0 !important;
            cursor: default !important;
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }

        /* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
        .a6S {
           display: none !important;
           opacity: 0.01 !important;
       }
       /* If the above doesn't work, add a .g-img class to any image in question. */
       img.g-img + div {
           display: none !important;
       }

       /* What it does: Prevents underlining the button text in Windows 10 */
        .button-link {
            text-decoration: none !important;
        }

        /* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
        /* Create one of these media queries for each additional viewport size you'd like to fix */

        /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
        @media only screen and (min-device-width: 320px) and (max-device-width: 374px) {
            .email-container {
                min-width: 320px !important;
            }
        }
        /* iPhone 6, 6S, 7, 8, and X */
        @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
            .email-container {
                min-width: 375px !important;
            }
        }
        /* iPhone 6+, 7+, and 8+ */
        @media only screen and (min-device-width: 414px) {
            .email-container {
                min-width: 414px !important;
            }
        }

    </style>
    <!-- CSS Reset : END -->
	<!-- Reset list spacing because Outlook ignores much of our inline CSS. -->
	<!--[if mso]>
	<style type="text/css">
		ul,
		ol {
			margin: 0 !important;
		}
		li {
			margin-left: 30px !important;
		}
		li.list-item-first {
			margin-top: 0 !important;
		}
		li.list-item-last {
			margin-bottom: 10px !important;
		}
	</style>
	<![endif]-->

    <!-- Progressive Enhancements : BEGIN -->
    <style>

        /* What it does: Hover styles for buttons */
        .button-td,
        .button-a {
            transition: all 100ms ease-in;
        }
	    .button-td-primary:hover,
	    .button-a-primary:hover {
	        background: #555555 !important;
	        border-color: #555555 !important;
	    }

        /* Media Queries */
        @media screen and (max-width: 600px) {

            .email-container {
                width: 100% !important;
                margin: auto !important;
            }

            /* What it does: Forces elements to resize to the full width of their container. Useful for resizing images beyond their max-width. */
            .fluid {
                max-width: 100% !important;
                height: auto !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            /* What it does: Forces table cells into full-width rows. */
            .stack-column,
            .stack-column-center {
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                direction: ltr !important;
            }
            /* And center justify these ones. */
            .stack-column-center {
                text-align: center !important;
            }

            /* What it does: Generic utility class for centering. Useful for images, buttons, and nested tables. */
            .center-on-narrow {
                text-align: center !important;
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
                float: none !important;
            }
            table.center-on-narrow {
                display: inline-block !important;
            }

            /* What it does: Adjust typography on small screens to improve readability */
            .email-container p {
                font-size: 17px !important;
            }
        }

    </style>
    <!-- Progressive Enhancements : END -->

    <!-- What it does: Makes background images in 72ppi Outlook render at correct size. -->
    <!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->

</head>
<!--
	The email background color (#222222) is defined in three places:
	1. body tag: for most email clients
	2. center tag: for Gmail and Inbox mobile apps and web versions of Gmail, GSuite, Inbox, Yahoo, AOL, Libero, Comcast, freenet, Mail.ru, Orange.fr
	3. mso conditional: For Windows 10 Mail
-->
<body width="100%" style="margin: 0; mso-line-height-rule: exactly; background-color: #ffffff;">
    <center style="width: 100%; background-color: #ffffff; text-align: left;">
    <!--[if mso | IE]>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #222222;">
    <tr>
    <td>
    <![endif]-->

        <!-- Visually Hidden Preheader Text : BEGIN -->
        <!-- Visually Hidden Preheader Text : END -->

        <!-- Create white space after the desired preview text so email clients don’t pull other distracting text into the inbox preview. Extend as necessary. -->
        <!-- Preview Text Spacing Hack : BEGIN -->
        <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
	        &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
        </div>
        <!-- Preview Text Spacing Hack : END -->

        <!-- Email Body : BEGIN -->
        <table align="center" role="presentation" cellspacing="0" cellpadding="10" border="0" width="600" style="margin: 0 auto;" class="email-container">
	        <!-- Email Header : BEGIN -->
	        <!-- Email Header : END -->

            <!-- Hero Image, Flush : BEGIN -->
            <tr>
                <td style="background-color: #ffffff;">
                    <img src="https://moneyconf.com/wp-content/themes/moneyconf/dist/images/logo17-white.png" width="600" height="" alt="alt_text" border="0" style="width: 100%; max-width: 600px; height: auto; background: #00b3e3; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555; margin: auto;" class="g-img">
                </td>
            </tr>
            <!-- Hero Image, Flush : END -->

            <!-- 1 Column Text + Button : BEGIN -->
            <tr>
                <td style="background-color: #ffffff;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <h1 style="margin: 0 0 10px; font-size: 24px; line-height: 125%; color: #333333; font-weight: normal;">You talk from MoneyConf is now live on Facebook</h1>
                                <p style="margin: 0 0 10px;">Please find the link to your talk at the button below.</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 0 20px 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <!-- Button : BEGIN -->
                                <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: auto;">
                                    <tr>
                                        <td class="button-td button-td-primary" style="border-radius: 4px; background: #222222;">
										     <a class="button-a button-a-primary" href="{}" style="background: #00b3e3;; border: 1px solid #00b3e3;; font-family: sans-serif; font-size: 15px; line-height: 15px; text-decoration: none; padding: 13px 17px; display: block; border-radius: 4px;"><span class="button-link" style="color:#ffffff">Talk on Facebook</span></a>
										</td>
                                    </tr>
                                </table>
								<!-- Button : END -->
								<p style="margin: 10 0 10px;"> We do ask that you include "© MoneyConf" or "courtesy of MoneyConf" when posting your videos online. If you would like to tag our accounts in your video posts on social media our accounts are - Twitter <a href="https://twitter.com/MoneyConfHQ">https://twitter.com/MoneyConfHQ</a>, Facebook <a href = " https://www.facebook.com/MoneyConf/"> https://www.facebook.com/MoneyConf/ </a> we can then share this post on our accounts to our online audience. We also recommend that you use the hashtag #MoneyConf to ensure your post reaches the attendees from the event.   </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
            <!-- 1 Column Text + Button : END -->

        <!-- Clear Spacer : BEGIN -->
	        <tr>
	            <td aria-hidden="true" height="40" style="font-size: 0; line-height: 0;">
	                &nbsp;
	            </td>
	        </tr>
	        <!-- Clear Spacer : END -->

	    </table>
	    <!-- Email Body : END -->


		<!--[if mso | IE]>
    </td>
    </tr>
    </table>
    <![endif]-->
    </center>
</body>
</html>

"""


def html_email_processing(facebook_url):
    return html_email.format(facebook_url)


def html_email_processing_2(facebook_url):
    html_email_1 = """
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->

    <!-- Web Font / @font-face : BEGIN -->
    <!-- NOTE: If web fonts are not required, lines 10 - 27 can be safely removed. -->

    <!-- Desktop Outlook chokes on web font references and defaults to Times New Roman, so we force a safe fallback font. -->
    <!--[if mso]>
        <style>
            * {
                font-family: sans-serif !important;
            }
        </style>
    <![endif]-->

    <!-- All other clients get the webfont reference; some will render the font and others will silently fail to the fallbacks. More on that here: http://stylecampaign.com/blog/2015/02/webfont-support-in-email/ -->
    <!--[if !mso]><!-->
    <!-- insert web font reference, eg: <link href='https://fonts.googleapis.com/css?family=Roboto:400,700' rel='stylesheet' type='text/css'> -->
    <!--<![endif]-->

    <!-- Web Font / @font-face : END -->

    <!-- CSS Reset : BEGIN -->
    <style>

        /* What it does: Remove spaces around the email design added by some email clients. */
        /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */
        html,
        body {
            margin: 0 auto !important;
            padding: 0 !important;
            height: 100% !important;
            width: 100% !important;
        }

        /* What it does: Stops email clients resizing small text. */
        * {
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%;
        }

        /* What it does: Centers email on Android 4.4 */
        div[style*="margin: 16px 0"] {
            margin: 0 !important;
        }

        /* What it does: Stops Outlook from adding extra spacing to tables. */
        table,
        td {
            mso-table-lspace: 0pt !important;
            mso-table-rspace: 0pt !important;
        }

        /* What it does: Fixes webkit padding issue. Fix for Yahoo mail table alignment bug. Applies table-layout to the first 2 tables then removes for anything nested deeper. */
        table {
            border-spacing: 0 !important;
            border-collapse: collapse !important;
            table-layout: fixed !important;
            margin: 0 auto !important;
        }
        table table table {
            table-layout: auto;
        }

        /* What it does: Uses a better rendering method when resizing images in IE. */
        img {
            -ms-interpolation-mode:bicubic;
        }

        /* What it does: A work-around for email clients meddling in triggered links. */
        *[x-apple-data-detectors],  /* iOS */
        .unstyle-auto-detected-links *,
        .aBn {
            border-bottom: 0 !important;
            cursor: default !important;
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }

        /* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
        .a6S {
           display: none !important;
           opacity: 0.01 !important;
       }
       /* If the above doesn't work, add a .g-img class to any image in question. */
       img.g-img + div {
           display: none !important;
       }

       /* What it does: Prevents underlining the button text in Windows 10 */
        .button-link {
            text-decoration: none !important;
        }

        /* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
        /* Create one of these media queries for each additional viewport size you'd like to fix */

        /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
        @media only screen and (min-device-width: 320px) and (max-device-width: 374px) {
            .email-container {
                min-width: 320px !important;
            }
        }
        /* iPhone 6, 6S, 7, 8, and X */
        @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
            .email-container {
                min-width: 375px !important;
            }
        }
        /* iPhone 6+, 7+, and 8+ */
        @media only screen and (min-device-width: 414px) {
            .email-container {
                min-width: 414px !important;
            }
        }

    </style>
    <!-- CSS Reset : END -->
	<!-- Reset list spacing because Outlook ignores much of our inline CSS. -->
	<!--[if mso]>
	<style type="text/css">
		ul,
		ol {
			margin: 0 !important;
		}
		li {
			margin-left: 30px !important;
		}
		li.list-item-first {
			margin-top: 0 !important;
		}
		li.list-item-last {
			margin-bottom: 10px !important;
		}
	</style>
	<![endif]-->

    <!-- Progressive Enhancements : BEGIN -->
    <style>

        /* What it does: Hover styles for buttons */
        .button-td,
        .button-a {
            transition: all 100ms ease-in;
        }
	    .button-td-primary:hover,
	    .button-a-primary:hover {
	        background: #555555 !important;
	        border-color: #555555 !important;
	    }

        /* Media Queries */
        @media screen and (max-width: 600px) {

            .email-container {
                width: 100% !important;
                margin: auto !important;
            }

            /* What it does: Forces elements to resize to the full width of their container. Useful for resizing images beyond their max-width. */
            .fluid {
                max-width: 100% !important;
                height: auto !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            /* What it does: Forces table cells into full-width rows. */
            .stack-column,
            .stack-column-center {
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                direction: ltr !important;
            }
            /* And center justify these ones. */
            .stack-column-center {
                text-align: center !important;
            }

            /* What it does: Generic utility class for centering. Useful for images, buttons, and nested tables. */
            .center-on-narrow {
                text-align: center !important;
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
                float: none !important;
            }
            table.center-on-narrow {
                display: inline-block !important;
            }

            /* What it does: Adjust typography on small screens to improve readability */
            .email-container p {
                font-size: 17px !important;
            }
        }

    </style>
    <!-- Progressive Enhancements : END -->

    <!-- What it does: Makes background images in 72ppi Outlook render at correct size. -->
    <!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->

</head>
<!--
	The email background color (#222222) is defined in three places:
	1. body tag: for most email clients
	2. center tag: for Gmail and Inbox mobile apps and web versions of Gmail, GSuite, Inbox, Yahoo, AOL, Libero, Comcast, freenet, Mail.ru, Orange.fr
	3. mso conditional: For Windows 10 Mail
-->
<body width="100%" style="margin: 0; mso-line-height-rule: exactly; background-color: #ffffff;">
    <center style="width: 100%; background-color: #ffffff; text-align: left;">
    <!--[if mso | IE]>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #222222;">
    <tr>
    <td>
    <![endif]-->

        <!-- Visually Hidden Preheader Text : BEGIN -->
        <!-- Visually Hidden Preheader Text : END -->

        <!-- Create white space after the desired preview text so email clients don’t pull other distracting text into the inbox preview. Extend as necessary. -->
        <!-- Preview Text Spacing Hack : BEGIN -->
        <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
	        &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
        </div>
        <!-- Preview Text Spacing Hack : END -->

        <!-- Email Body : BEGIN -->
        <table align="center" role="presentation" cellspacing="0" cellpadding="10" border="0" width="600" style="margin: 0 auto;" class="email-container">
	        <!-- Email Header : BEGIN -->
	        <!-- Email Header : END -->

            <!-- Hero Image, Flush : BEGIN -->
            <tr>
                <td style="background-color: #ffffff;">
                    <img src="https://moneyconf.com/wp-content/themes/moneyconf/dist/images/logo17-white.png" width="600" height="" alt="alt_text" border="0" style="width: 100%; max-width: 600px; height: auto; background: #00b3e3; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555; margin: auto;" class="g-img">
                </td>
            </tr>
            <!-- Hero Image, Flush : END -->

            <!-- 1 Column Text + Button : BEGIN -->
            <tr>
                <td style="background-color: #ffffff;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <h1 style="margin: 0 0 10px; font-size: 24px; line-height: 125%; color: #333333; font-weight: normal;">You talk from MoneyConf is now live on Facebook</h1>
                                <p style="margin: 0 0 10px;">Please find the link to your talk at the button below.</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 0 20px 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <!-- Button : BEGIN -->
                                <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: auto;">
                                    <tr>
                                        <td class="button-td button-td-primary" style="border-radius: 4px; background: #222222;">""" 
    
    html_email_2 =				    """<a class="button-a button-a-primary" href="{}" style="background: #00b3e3;; border: 1px solid #00b3e3;; font-family: sans-serif; font-size: 15px; line-height: 15px; text-decoration: none; padding: 13px 17px; display: block; border-radius: 4px;"><span class="button-link" style="color:#ffffff">Talk on Facebook</span></a>"""
									
    html_email_3 =              """                  	</td>
                                    </tr>
                                </table>
								<!-- Button : END -->
								<p style="margin: 10 0 10px;"> We do ask that you include "© MoneyConf" or "courtesy of MoneyConf" when posting your videos online. If you would like to tag our accounts in your video posts on social media our accounts are - Twitter <a href="https://twitter.com/MoneyConfHQ">https://twitter.com/MoneyConfHQ</a>, Facebook <a href = " https://www.facebook.com/MoneyConf/"> https://www.facebook.com/MoneyConf/ </a> we can then share this post on our accounts to our online audience. We also recommend that you use the hashtag #MoneyConf to ensure your post reaches the attendees from the event.   </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
            <!-- 1 Column Text + Button : END -->

        <!-- Clear Spacer : BEGIN -->
	        <tr>
	            <td aria-hidden="true" height="40" style="font-size: 0; line-height: 0;">
	                &nbsp;
	            </td>
	        </tr>
	        <!-- Clear Spacer : END -->

	    </table>
	    <!-- Email Body : END -->


		<!--[if mso | IE]>
    </td>
    </tr>
    </table>
    <![endif]-->
    </center>
</body>
</html>

"""
    return  html_email_1 + html_email_2.format(facebook_url) + html_email_3


#def html_email_processing_3(facebook_url):
#    html_email_1 = """
#<!DOCTYPE html>
#<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
#<head>
#    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
#    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
#    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
#    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
#    <title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->
#
#    <!-- Web Font / @font-face : BEGIN -->
#    <!-- NOTE: If web fonts are not required, lines 10 - 27 can be safely removed. -->
#
#    <!-- Desktop Outlook chokes on web font references and defaults to Times New Roman, so we force a safe fallback font. -->
#    <!--[if mso]>
#        <style>
#            * {
#                font-family: sans-serif !important;
#            }
#        </style>
#    <![endif]-->
#
#    <!-- All other clients get the webfont reference; some will render the font and others will silently fail to the fallbacks. More on that here: http://stylecampaign.com/blog/2015/02/webfont-support-in-email/ -->
#    <!--[if !mso]><!-->
#    <!-- insert web font reference, eg: <link href='https://fonts.googleapis.com/css?family=Roboto:400,700' rel='stylesheet' type='text/css'> -->
#    <!--<![endif]-->
#
#    <!-- Web Font / @font-face : END -->
#
#    <!-- CSS Reset : BEGIN -->
#    <style>
#
#        /* What it does: Remove spaces around the email design added by some email clients. */
#        /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */
#        html,
#        body {
#            margin: 0 auto !important;
#            padding: 0 !important;
#            height: 100% !important;
#            width: 100% !important;
#        }
#
#        /* What it does: Stops email clients resizing small text. */
#        * {
#            -ms-text-size-adjust: 100%;
#            -webkit-text-size-adjust: 100%;
#        }
#
#        /* What it does: Centers email on Android 4.4 */
#        div[style*="margin: 16px 0"] {
#            margin: 0 !important;
#        }
#
#        /* What it does: Stops Outlook from adding extra spacing to tables. */
#        table,
#        td {
#            mso-table-lspace: 0pt !important;
#            mso-table-rspace: 0pt !important;
#        }
#
#        /* What it does: Fixes webkit padding issue. Fix for Yahoo mail table alignment bug. Applies table-layout to the first 2 tables then removes for anything nested deeper. */
#        table {
#            border-spacing: 0 !important;
#            border-collapse: collapse !important;
#            table-layout: fixed !important;
#            margin: 0 auto !important;
#        }
#        table table table {
#            table-layout: auto;
#        }
#
#        /* What it does: Uses a better rendering method when resizing images in IE. */
#        img {
#            -ms-interpolation-mode:bicubic;
#        }
#
#        /* What it does: A work-around for email clients meddling in triggered links. */
#        *[x-apple-data-detectors],  /* iOS */
#        .unstyle-auto-detected-links *,
#        .aBn {
#            border-bottom: 0 !important;
#            cursor: default !important;
#            color: inherit !important;
#            text-decoration: none !important;
#            font-size: inherit !important;
#            font-family: inherit !important;
#            font-weight: inherit !important;
#            line-height: inherit !important;
#        }
#
#        /* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
#        .a6S {
#           display: none !important;
#           opacity: 0.01 !important;
#       }
#       /* If the above doesn't work, add a .g-img class to any image in question. */
#       img.g-img + div {
#           display: none !important;
#       }
#
#       /* What it does: Prevents underlining the button text in Windows 10 */
#        .button-link {
#            text-decoration: none !important;
#        }
#
#        /* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
#        /* Create one of these media queries for each additional viewport size you'd like to fix */
#
#        /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
#        @media only screen and (min-device-width: 320px) and (max-device-width: 374px) {
#            .email-container {
#                min-width: 320px !important;
#            }
#        }
#        /* iPhone 6, 6S, 7, 8, and X */
#        @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
#            .email-container {
#                min-width: 375px !important;
#            }
#        }
#        /* iPhone 6+, 7+, and 8+ */
#        @media only screen and (min-device-width: 414px) {
#            .email-container {
#                min-width: 414px !important;
#            }
#        }
#
#    </style>
#    <!-- CSS Reset : END -->
#	<!-- Reset list spacing because Outlook ignores much of our inline CSS. -->
#	<!--[if mso]>
#	<style type="text/css">
#		ul,
#		ol {
#			margin: 0 !important;
#		}
#		li {
#			margin-left: 30px !important;
#		}
#		li.list-item-first {
#			margin-top: 0 !important;
#		}
#		li.list-item-last {
#			margin-bottom: 10px !important;
#		}
#	</style>
#	<![endif]-->
#
#    <!-- Progressive Enhancements : BEGIN -->
#    <style>
#
#        /* What it does: Hover styles for buttons */
#        .button-td,
#        .button-a {
#            transition: all 100ms ease-in;
#        }
#	    .button-td-primary:hover,
#	    .button-a-primary:hover {
#	        background: #555555 !important;
#	        border-color: #555555 !important;
#	    }
#
#        /* Media Queries */
#        @media screen and (max-width: 600px) {
#
#            .email-container {
#                width: 100% !important;
#                margin: auto !important;
#            }
#
#            /* What it does: Forces elements to resize to the full width of their container. Useful for resizing images beyond their max-width. */
#            .fluid {
#                max-width: 100% !important;
#                height: auto !important;
#                margin-left: auto !important;
#                margin-right: auto !important;
#            }
#
#            /* What it does: Forces table cells into full-width rows. */
#            .stack-column,
#            .stack-column-center {
#                display: block !important;
#                width: 100% !important;
#                max-width: 100% !important;
#                direction: ltr !important;
#            }
#            /* And center justify these ones. */
#            .stack-column-center {
#                text-align: center !important;
#            }
#
#            /* What it does: Generic utility class for centering. Useful for images, buttons, and nested tables. */
#            .center-on-narrow {
#                text-align: center !important;
#                display: block !important;
#                margin-left: auto !important;
#                margin-right: auto !important;
#                float: none !important;
#            }
#            table.center-on-narrow {
#                display: inline-block !important;
#            }
#
#            /* What it does: Adjust typography on small screens to improve readability */
#            .email-container p {
#                font-size: 17px !important;
#            }
#        }
#
#    </style>
#    <!-- Progressive Enhancements : END -->
#
#    <!-- What it does: Makes background images in 72ppi Outlook render at correct size. -->
#    <!--[if gte mso 9]>
#    <xml>
#        <o:OfficeDocumentSettings>
#            <o:AllowPNG/>
#            <o:PixelsPerInch>96</o:PixelsPerInch>
#        </o:OfficeDocumentSettings>
#    </xml>
#    <![endif]-->
#
#</head>
#<!--
#	The email background color (#222222) is defined in three places:
#	1. body tag: for most email clients
#	2. center tag: for Gmail and Inbox mobile apps and web versions of Gmail, GSuite, Inbox, Yahoo, AOL, Libero, Comcast, freenet, Mail.ru, Orange.fr
#	3. mso conditional: For Windows 10 Mail
#-->
#<body width="100%" style="margin: 0; mso-line-height-rule: exactly; background-color: #ffffff;">
#    <center style="width: 100%; background-color: #ffffff; text-align: left;">
#    <!--[if mso | IE]>
#    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #222222;">
#    <tr>
#    <td>
#    <![endif]-->
#
#        <!-- Visually Hidden Preheader Text : BEGIN -->
#        <!-- Visually Hidden Preheader Text : END -->
#
#        <!-- Create white space after the desired preview text so email clients don’t pull other distracting text into the inbox preview. Extend as necessary. -->
#        <!-- Preview Text Spacing Hack : BEGIN -->
#        <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
#	        &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
#        </div>
#        <!-- Preview Text Spacing Hack : END -->
#
#        <!-- Email Body : BEGIN -->
#        <table align="center" role="presentation" cellspacing="0" cellpadding="10" border="0" width="600" style="margin: 0 auto;" class="email-container">
#	        <!-- Email Header : BEGIN -->
#	        <!-- Email Header : END -->
#
#            <!-- Hero Image, Flush : BEGIN -->
#            <tr>
#                <td style="background-color: #ffffff;">
#                    <img src="https://moneyconf.com/wp-content/themes/moneyconf/dist/images/logo17-white.png" width="600" height="" alt="alt_text" border="0" style="width: 100%; max-width: 600px; height: auto; background: #00b3e3; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555; margin: auto;" class="g-img">
#                </td>
#            </tr>
#            <!-- Hero Image, Flush : END -->
#
#            <!-- 1 Column Text + Button : BEGIN -->
#            <tr>
#                <td style="background-color: #ffffff;">
#                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
#                        <tr>
#                            <td style="padding: 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
#                                <h1 style="margin: 0 0 10px; font-size: 24px; line-height: 125%; color: #333333; font-weight: normal;">You talk from MoneyConf is now live on Facebook</h1>
#                                <p style="margin: 0 0 10px;">Please find the link to your talk at the button below.</p>
#                            </td>
#                        </tr>
#                        <tr>
#                            <td style="padding: 0 20px 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
#                                <!-- Button : BEGIN -->
#                                <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: auto;">
#                                    <tr>
#                                        <td class="button-td button-td-primary" style="border-radius: 4px; background: #222222;">""" 
#    
#    html_email_2 =				    """<a class="button-a button-a-primary" href="{}" style="background: #00b3e3;; border: 1px solid #00b3e3;; font-family: sans-serif; font-size: 15px; line-height: 15px; text-decoration: none; padding: 13px 17px; display: block; border-radius: 4px;"><span class="button-link" style="color:#ffffff">Talk on Facebook</span></a>"""
#									
#    html_email_3 =              """                  	</td>
#                                    </tr>
#                                </table>
#								<!-- Button : END -->
#								<p style="margin: 10 0 10px;"> Your MoneyConf talk can be found at this link: <a href="{}">{}</a>. We do ask that you include "© MoneyConf" or "courtesy of MoneyConf" when posting your videos online. If you would like to tag our accounts in your video posts on social media our accounts are - Twitter <a href="https://twitter.com/MoneyConfHQ">https://twitter.com/MoneyConfHQ</a>, Facebook <a href = " https://www.facebook.com/MoneyConf/"> https://www.facebook.com/MoneyConf/ </a> we can then share this post on our accounts to our online audience. We also recommend that you use the hashtag #MoneyConf to ensure your post reaches the attendees from the event.   </p>
#                            </td>
#                        </tr>
#                                """
#    html_email_4 = """                </table>
#                </td>
#            </tr>
#            <!-- 1 Column Text + Button : END -->
#
#        <!-- Clear Spacer : BEGIN -->
#	        <tr>
#	            <td aria-hidden="true" height="40" style="font-size: 0; line-height: 0;">
#	                &nbsp;
#	            </td>
#	        </tr>
#	        <!-- Clear Spacer : END -->
#
#	    </table>
#	    <!-- Email Body : END -->
#
#
#		<!--[if mso | IE]>
#    </td>
#    </tr>
#    </table>
#    <![endif]-->
#    </center>
#</body>
#</html>
#
#"""
#    return  html_email_1 + html_email_2.format(facebook_url) + html_email_3.format(facebook_url,facebook_url) + html_email_4



def html_email_processing_3(facebook_url):
    html_email_1 = """
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->

    <!-- Web Font / @font-face : BEGIN -->
    <!-- NOTE: If web fonts are not required, lines 10 - 27 can be safely removed. -->

    <!-- Desktop Outlook chokes on web font references and defaults to Times New Roman, so we force a safe fallback font. -->
    <!--[if mso]>
        <style>
            * {
                font-family: sans-serif !important;
            }
        </style>
    <![endif]-->

    <!-- All other clients get the webfont reference; some will render the font and others will silently fail to the fallbacks. More on that here: http://stylecampaign.com/blog/2015/02/webfont-support-in-email/ -->
    <!--[if !mso]><!-->
    <!-- insert web font reference, eg: <link href='https://fonts.googleapis.com/css?family=Roboto:400,700' rel='stylesheet' type='text/css'> -->
    <!--<![endif]-->

    <!-- Web Font / @font-face : END -->

    <!-- CSS Reset : BEGIN -->
    <style>

        /* What it does: Remove spaces around the email design added by some email clients. */
        /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */
        html,
        body {
            margin: 0 auto !important;
            padding: 0 !important;
            height: 100% !important;
            width: 100% !important;
        }

        /* What it does: Stops email clients resizing small text. */
        * {
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%;
        }

        /* What it does: Centers email on Android 4.4 */
        div[style*="margin: 16px 0"] {
            margin: 0 !important;
        }

        /* What it does: Stops Outlook from adding extra spacing to tables. */
        table,
        td {
            mso-table-lspace: 0pt !important;
            mso-table-rspace: 0pt !important;
        }

        /* What it does: Fixes webkit padding issue. Fix for Yahoo mail table alignment bug. Applies table-layout to the first 2 tables then removes for anything nested deeper. */
        table {
            border-spacing: 0 !important;
            border-collapse: collapse !important;
            table-layout: fixed !important;
            margin: 0 auto !important;
        }
        table table table {
            table-layout: auto;
        }

        /* What it does: Uses a better rendering method when resizing images in IE. */
        img {
            -ms-interpolation-mode:bicubic;
        }

        /* What it does: A work-around for email clients meddling in triggered links. */
        *[x-apple-data-detectors],  /* iOS */
        .unstyle-auto-detected-links *,
        .aBn {
            border-bottom: 0 !important;
            cursor: default !important;
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }

        /* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
        .a6S {
           display: none !important;
           opacity: 0.01 !important;
       }
       /* If the above doesn't work, add a .g-img class to any image in question. */
       img.g-img + div {
           display: none !important;
       }

       /* What it does: Prevents underlining the button text in Windows 10 */
        .button-link {
            text-decoration: none !important;
        }

        /* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
        /* Create one of these media queries for each additional viewport size you'd like to fix */

        /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
        @media only screen and (min-device-width: 320px) and (max-device-width: 374px) {
            .email-container {
                min-width: 320px !important;
            }
        }
        /* iPhone 6, 6S, 7, 8, and X */
        @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
            .email-container {
                min-width: 375px !important;
            }
        }
        /* iPhone 6+, 7+, and 8+ */
        @media only screen and (min-device-width: 414px) {
            .email-container {
                min-width: 414px !important;
            }
        }

    </style>
    <!-- CSS Reset : END -->
	<!-- Reset list spacing because Outlook ignores much of our inline CSS. -->
	<!--[if mso]>
	<style type="text/css">
		ul,
		ol {
			margin: 0 !important;
		}
		li {
			margin-left: 30px !important;
		}
		li.list-item-first {
			margin-top: 0 !important;
		}
		li.list-item-last {
			margin-bottom: 10px !important;
		}
	</style>
	<![endif]-->

    <!-- Progressive Enhancements : BEGIN -->
    <style>

        /* What it does: Hover styles for buttons */
        .button-td,
        .button-a {
            transition: all 100ms ease-in;
        }
	    .button-td-primary:hover,
	    .button-a-primary:hover {
	        background: #555555 !important;
	        border-color: #555555 !important;
	    }

        /* Media Queries */
        @media screen and (max-width: 600px) {

            .email-container {
                width: 100% !important;
                margin: auto !important;
            }

            /* What it does: Forces elements to resize to the full width of their container. Useful for resizing images beyond their max-width. */
            .fluid {
                max-width: 100% !important;
                height: auto !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            /* What it does: Forces table cells into full-width rows. */
            .stack-column,
            .stack-column-center {
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                direction: ltr !important;
            }
            /* And center justify these ones. */
            .stack-column-center {
                text-align: center !important;
            }

            /* What it does: Generic utility class for centering. Useful for images, buttons, and nested tables. */
            .center-on-narrow {
                text-align: center !important;
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
                float: none !important;
            }
            table.center-on-narrow {
                display: inline-block !important;
            }

            /* What it does: Adjust typography on small screens to improve readability */
            .email-container p {
                font-size: 17px !important;
            }
        }

    </style>
    <!-- Progressive Enhancements : END -->

    <!-- What it does: Makes background images in 72ppi Outlook render at correct size. -->
    <!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->

</head>
<!--
	The email background color (#222222) is defined in three places:
	1. body tag: for most email clients
	2. center tag: for Gmail and Inbox mobile apps and web versions of Gmail, GSuite, Inbox, Yahoo, AOL, Libero, Comcast, freenet, Mail.ru, Orange.fr
	3. mso conditional: For Windows 10 Mail
-->
<body width="100%" style="margin: 0; mso-line-height-rule: exactly; background-color: #ffffff;">
    <center style="width: 100%; background-color: #ffffff; text-align: left;">
    <!--[if mso | IE]>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #222222;">
    <tr>
    <td>
    <![endif]-->

        <!-- Visually Hidden Preheader Text : BEGIN -->
        <!-- Visually Hidden Preheader Text : END -->

        <!-- Create white space after the desired preview text so email clients don’t pull other distracting text into the inbox preview. Extend as necessary. -->
        <!-- Preview Text Spacing Hack : BEGIN -->
        <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
	        &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
        </div>
        <!-- Preview Text Spacing Hack : END -->

        <!-- Email Body : BEGIN -->
        <table align="center" role="presentation" cellspacing="0" cellpadding="10" border="0" width="600" style="margin: 0 auto;" class="email-container">
	        <!-- Email Header : BEGIN -->
	        <!-- Email Header : END -->

            <!-- Hero Image, Flush : BEGIN -->
            
             <tr>
                <td style="background-color: #EF4343;">
                    
    <a href="https://riseconf.com" class="hero-branding">
        <svg class="rise-logo" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 289.3 90.8" enable-background="new 0 0 289.3 90.8" xml:space="preserve">
        <g>
        
        <path class="rise-text" fill="#fff" d="M0,20.7c0,21.8,0,43.6,0,65.5c0,0.4,0,0.7,0,1.1c0,0.7,0,1.5,0,2.3c7.2,0,14.3,0,21.5,0c0-3,0-6.1,0-9.1
                c0-6.1,0-12.1,0-18.2c0.2,0,0.3,0,0.5,0c3.9,0,7.9,0,11.8,0c0.4,0,0.5,0.2,0.7,0.4c2.7,4,5.4,8.1,8.1,12.1c1,1.5,2,2.9,3,4.4
                c1.7,2.5,3.4,5,5,7.5c0.4,0.7,0.9,1.3,1.3,2c0.5,0.7,1,1,1.9,1c7.3,0,14.6,0,21.9,0c0.8,0,1.6,0,2.5,0c-1.5-2.2-3.1-4.5-4.6-6.7
                c-3.2-4.7-6.4-9.3-9.5-13.9c-2.4-3.5-4.8-7.1-7.3-10.6c0.1-0.1,0.2-0.1,0.3-0.1c3.9-1.7,7.3-4.2,10.3-7.3c3-3.1,5-6.8,6-11
                c0.9-3.5,1-7.1,0.9-10.6c-0.1-2.8-0.4-5.6-1.2-8.3c-2.4-8-7.8-13.4-15.3-16.8c-4.9-2.2-10.2-3-15.6-3c-12.4,0-24.9,0-37.3,0
                c-1.5,0-2.9,0-4.4-0.1C0.1,1.1,0,1.2,0,1.6C0,2.8,0,4,0,5.2C0,10.4,0,15.6,0,20.7z M20,88H1.5v-0.6l18.4-5V88z M69.2,79.2l1.7,2.5
                l-19.6,3.2l-3.4-5.1l-1.1-1.6L45.4,76l-0.3-0.4l18.3-4.9L69.2,79.2z M18.8,18.2c0.7,0,1.5,0,2.3,0c6.2,0,12.4,0,18.6,0
                c2.5,0,5,0.3,7.4,1.2c3.8,1.5,6.7,4,7.7,8.2c0.8,3.3,0.9,6.8-0.5,10c-1.8,4-4.9,6.4-9.1,7.4c-1.8,0.4-3.7,0.6-5.5,0.5
                c-4.6,0-9.1,0-13.7,0c-2.1,0-4.2,0-6.4,0.1c-0.2,0-0.4,0-0.7,0C18.8,36.5,18.8,27.4,18.8,18.2z"></path>
        
        <path class="rise-text" fill="#fff" d="M115.3,76.1c0-7,0-14,0-21c0-18,0-35.9,0-53.9c-7.2,0-14.2,0-21.4,0c0,19.9,0,39.8,0,59.7
                c0,6.2,0,12.5,0,18.7c0,3.3,0,6.6,0,9.9c7.2,0,14.3,0,21.4,0C115.3,85,115.3,80.6,115.3,76.1z M95.5,77.8V62l18.3-4.9v17.7
                L95.5,77.8z"></path>
        
        <path class="rise-text" fill="#fff" d="M163.8,90.4c1.1,0.1,2.2,0.2,3.4,0.3c2.1,0,4.1,0,6.2,0c0.2,0,0.3-0.1,0.5-0.1c1.7-0.2,3.4-0.3,5.1-0.6
                c4.4-0.7,8.6-2.1,12.3-4.6c5.9-3.9,9.9-9.1,11.3-16.1c0.5-2.5,0.6-5,0.6-7.5c0-1.2-0.1-2.3-0.2-3.5c-0.3-3.2-1.3-6.2-3.2-8.9
                c-2.5-3.6-5.7-6.3-9.5-8.3c-2.9-1.6-6-2.8-9.2-3.8c-0.3-0.1-0.7-0.2-1-0.3c-4.3-1.3-8.6-2.4-12.9-3.7c-2.4-0.7-4.8-1.5-6.9-2.7
                c-1.8-1-2.6-2.6-2.8-4.5c-0.2-2.2,1.1-4.4,3.3-5.5c2.2-1.1,4.6-1.4,7-1.3c2.3,0.1,4.6,0.5,6.9,1.2c4.9,1.6,9.3,4,13.6,6.8
                c0.5,0.3,1,0.7,1.6,1.1c3.8-5.5,7.6-11,11.5-16.6c-1.8-1.3-3.5-2.7-5.4-3.9c-6.6-4.3-13.9-6.9-21.8-7.7c-1.1-0.1-2.3-0.2-3.4-0.3
                c-2.1,0-4.1,0-6.2,0c-0.1,0-0.3,0.1-0.4,0.1c-1.6,0.2-3.2,0.3-4.7,0.6c-6.4,1.2-11.9,3.8-16.4,8.6c-3.8,4-6,8.6-6.6,14.1
                c-0.3,2.8-0.3,5.7,0,8.5c0.3,3,1.1,5.8,2.7,8.4c1.6,2.7,3.8,5,6.3,6.8c0.9,0.6,1.8,1.2,2.8,1.8c3.6,2,7.4,3.3,11.3,4.4
                c3.9,1.1,7.8,2.1,11.8,3.2c2.7,0.8,5.4,1.7,7.8,3.2c0.6,0.3,1.1,0.7,1.6,1.2c1,1.2,1.4,2.9,1.2,4.4c-0.2,1.5-1,2.9-2.2,3.8
                c-2.1,1.5-4.4,2-6.9,2.2c-4.1,0.3-8-0.2-11.9-1.5c-0.7-0.2-1.3-0.5-2-0.7c-4.7-1.9-8.9-4.6-12.8-7.8c-0.3-0.3-0.6-0.5-1.1-0.9
                c-3.6,4.2-7.1,8.5-10.7,12.7c-0.8,0.9-1.6,1.9-2.4,2.8c1,0.9,2,1.8,3.1,2.7C143.4,85.5,153.1,89.3,163.8,90.4z M181.6,59.9
                c-0.6-0.7-1.3-1.1-1.9-1.5c-2.2-1.4-4.8-2.4-8.2-3.4c-1.9-0.5-3.8-1.1-5.7-1.6c-2-0.5-4-1.1-6-1.7c-3.5-1-7.3-2.2-10.8-4.2l32-8.6
                c3.3,1,6.1,2.2,8.5,3.5c3.9,2.1,6.8,4.6,9,7.8c1.6,2.3,2.6,5.1,2.9,8.2c0.1,0.7,0.1,1.4,0.2,2.1l-18.4,3
                C183,62.2,182.5,60.9,181.6,59.9z M138.7,70.1l6.4-7.6c2.9,2.4,5.7,4.3,8.6,5.8l-15.6,2.5L138.7,70.1z"></path>
        
        <path class="rise-text" fill="#fff" d="M289.3,70.2c-0.4,0-0.9,0-1.3,0c-14.9,0-29.8,0-44.6,0c-0.2,0-0.4,0-0.7,0c0-4.9,0-9.8,0-14.7l4.3-0.7
                c12,0,24.1,0,36.1,0c0-2,0-3.9,0-5.9c0-4.5,0-9,0-13.5c-13.5,0-26.9,0-40.4,0c0-4.9,0-9.7,0-14.6l0.8-0.2c15.1,0,30.1,0,45.1,0
                c0-4.1,0-8.1,0-12.2c0-2.4,0-4.8,0-7.2c-22.5,0-44.9,0-67.3,0c0,8.4,0,16.9,0,25.3c0,10.8,0,21.6,0,32.4c0,10.2,0,20.4,0,30.7
                c22.7,0,45.3,0,68,0C289.3,83.1,289.3,76.6,289.3,70.2z M287.1,19h-32l32-8.6V19z M281.5,36.9v10.7l-34.7,5.6l-5.7,0.9l-18.3,3
                V27.7l18.3-4.9v12.6v1.5h1.5H281.5z"></path>
        </g>
        </svg>
        </a>
                </td>
            </tr>
            <!-- Hero Image, Flush : END -->

            <!-- 1 Column Text + Button : BEGIN -->
            <tr>
                <td style="background-color: #ffffff;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <h1 style="margin: 0 0 10px; font-size: 24px; line-height: 125%; color: #333333; font-weight: normal;">You talk from RISE is now live on Facebook</h1>
                                <p style="margin: 0 0 10px;">Please find the link to your talk at the button below.</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 0 20px 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <!-- Button : BEGIN -->
                                <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: auto;">
                                    <tr>
                                        <td class="button-td button-td-primary" style="border-radius: 4px; background: #222222;">""" 
    
    html_email_2 =				    """<a class="button-a button-a-primary" href="{}" style="background: #EF4343;; border: 1px solid #00b3e3;; font-family: sans-serif; font-size: 15px; line-height: 15px; text-decoration: none; padding: 13px 17px; display: block; border-radius: 4px;"><span class="button-link" style="color:#ffffff">Talk on Facebook</span></a>"""
									
    html_email_3 =              """                  	</td>
                                    </tr>
                                </table>
								<!-- Button : END -->
								<p style="margin: 10 0 10px;"> Your RISE talk can be found at this link: <a href="{}">{}</a>. We do ask that you include "© RISE conf" or "courtesy of RISE conf" when posting your videos online. If you would like to tag our accounts in your video posts on social media our accounts are - Twitter <a href="https://twitter.com/riseconfhq">https://twitter.com/riseconfhq</a>, Facebook <a href = "https://www.facebook.com/RISEConfHQ/">https://www.facebook.com/RISEConfHQ/</a> and Instagram <a href = "https://www.instagram.com/riseconfhq/">https://www.instagram.com/riseconfhq/</a>. We can then share this post on our accounts to our online audience. We also recommend that you use the hashtag #RISEConf to ensure your post reaches the attendees from the event.   </p>
                            </td>
                        </tr>
                                """
    html_email_4 = """                </table>
                </td>
            </tr>
            <!-- 1 Column Text + Button : END -->

        <!-- Clear Spacer : BEGIN -->
	        <tr>
	            <td aria-hidden="true" height="40" style="font-size: 0; line-height: 0;">
	                &nbsp;
	            </td>
	        </tr>
	        <!-- Clear Spacer : END -->

	    </table>
	    <!-- Email Body : END -->


		<!--[if mso | IE]>
    </td>
    </tr>
    </table>
    <![endif]-->
    </center>
</body>
</html>

"""
    return  html_email_1 + html_email_2.format(facebook_url) + html_email_3.format(facebook_url,facebook_url) + html_email_4




def html_email_processing_4(youtube_url):
    html_email_1 = """
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->

    <!-- Web Font / @font-face : BEGIN -->
    <!-- NOTE: If web fonts are not required, lines 10 - 27 can be safely removed. -->

    <!-- Desktop Outlook chokes on web font references and defaults to Times New Roman, so we force a safe fallback font. -->
    <!--[if mso]>
        <style>
            * {
                font-family: sans-serif !important;
            }
        </style>
    <![endif]-->

    <!-- All other clients get the webfont reference; some will render the font and others will silently fail to the fallbacks. More on that here: http://stylecampaign.com/blog/2015/02/webfont-support-in-email/ -->
    <!--[if !mso]><!-->
    <!-- insert web font reference, eg: <link href='https://fonts.googleapis.com/css?family=Roboto:400,700' rel='stylesheet' type='text/css'> -->
    <!--<![endif]-->

    <!-- Web Font / @font-face : END -->

    <!-- CSS Reset : BEGIN -->
    <style>

        /* What it does: Remove spaces around the email design added by some email clients. */
        /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */
        html,
        body {
            margin: 0 auto !important;
            padding: 0 !important;
            height: 100% !important;
            width: 100% !important;
        }

        /* What it does: Stops email clients resizing small text. */
        * {
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%;
        }

        /* What it does: Centers email on Android 4.4 */
        div[style*="margin: 16px 0"] {
            margin: 0 !important;
        }

        /* What it does: Stops Outlook from adding extra spacing to tables. */
        table,
        td {
            mso-table-lspace: 0pt !important;
            mso-table-rspace: 0pt !important;
        }

        /* What it does: Fixes webkit padding issue. Fix for Yahoo mail table alignment bug. Applies table-layout to the first 2 tables then removes for anything nested deeper. */
        table {
            border-spacing: 0 !important;
            border-collapse: collapse !important;
            table-layout: fixed !important;
            margin: 0 auto !important;
        }
        table table table {
            table-layout: auto;
        }

        /* What it does: Uses a better rendering method when resizing images in IE. */
        img {
            -ms-interpolation-mode:bicubic;
        }

        /* What it does: A work-around for email clients meddling in triggered links. */
        *[x-apple-data-detectors],  /* iOS */
        .unstyle-auto-detected-links *,
        .aBn {
            border-bottom: 0 !important;
            cursor: default !important;
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }

        /* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
        .a6S {
           display: none !important;
           opacity: 0.01 !important;
       }
       /* If the above doesn't work, add a .g-img class to any image in question. */
       img.g-img + div {
           display: none !important;
       }

       /* What it does: Prevents underlining the button text in Windows 10 */
        .button-link {
            text-decoration: none !important;
        }

        /* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
        /* Create one of these media queries for each additional viewport size you'd like to fix */

        /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
        @media only screen and (min-device-width: 320px) and (max-device-width: 374px) {
            .email-container {
                min-width: 320px !important;
            }
        }
        /* iPhone 6, 6S, 7, 8, and X */
        @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
            .email-container {
                min-width: 375px !important;
            }
        }
        /* iPhone 6+, 7+, and 8+ */
        @media only screen and (min-device-width: 414px) {
            .email-container {
                min-width: 414px !important;
            }
        }

    </style>
    <!-- CSS Reset : END -->
	<!-- Reset list spacing because Outlook ignores much of our inline CSS. -->
	<!--[if mso]>
	<style type="text/css">
		ul,
		ol {
			margin: 0 !important;
		}
		li {
			margin-left: 30px !important;
		}
		li.list-item-first {
			margin-top: 0 !important;
		}
		li.list-item-last {
			margin-bottom: 10px !important;
		}
	</style>
	<![endif]-->

    <!-- Progressive Enhancements : BEGIN -->
    <style>

        /* What it does: Hover styles for buttons */
        .button-td,
        .button-a {
            transition: all 100ms ease-in;
        }
	    .button-td-primary:hover,
	    .button-a-primary:hover {
	        background: #555555 !important;
	        border-color: #555555 !important;
	    }

        /* Media Queries */
        @media screen and (max-width: 600px) {

            .email-container {
                width: 100% !important;
                margin: auto !important;
            }

            /* What it does: Forces elements to resize to the full width of their container. Useful for resizing images beyond their max-width. */
            .fluid {
                max-width: 100% !important;
                height: auto !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            /* What it does: Forces table cells into full-width rows. */
            .stack-column,
            .stack-column-center {
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                direction: ltr !important;
            }
            /* And center justify these ones. */
            .stack-column-center {
                text-align: center !important;
            }

            /* What it does: Generic utility class for centering. Useful for images, buttons, and nested tables. */
            .center-on-narrow {
                text-align: center !important;
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
                float: none !important;
            }
            table.center-on-narrow {
                display: inline-block !important;
            }

            /* What it does: Adjust typography on small screens to improve readability */
            .email-container p {
                font-size: 17px !important;
            }
        }

    </style>
    <!-- Progressive Enhancements : END -->

    <!-- What it does: Makes background images in 72ppi Outlook render at correct size. -->
    <!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->

</head>
<!--
	The email background color (#222222) is defined in three places:
	1. body tag: for most email clients
	2. center tag: for Gmail and Inbox mobile apps and web versions of Gmail, GSuite, Inbox, Yahoo, AOL, Libero, Comcast, freenet, Mail.ru, Orange.fr
	3. mso conditional: For Windows 10 Mail
-->
<body width="100%" style="margin: 0; mso-line-height-rule: exactly; background-color: #ffffff;">
    <center style="width: 100%; background-color: #ffffff; text-align: left;">
    <!--[if mso | IE]>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #222222;">
    <tr>
    <td>
    <![endif]-->

        <!-- Visually Hidden Preheader Text : BEGIN -->
        <!-- Visually Hidden Preheader Text : END -->

        <!-- Create white space after the desired preview text so email clients don’t pull other distracting text into the inbox preview. Extend as necessary. -->
        <!-- Preview Text Spacing Hack : BEGIN -->
        <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
	        &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
        </div>
        <!-- Preview Text Spacing Hack : END -->

        <!-- Email Body : BEGIN -->
        <table align="center" role="presentation" cellspacing="0" cellpadding="10" border="0" width="600" style="margin: 0 auto;" class="email-container">
	        <!-- Email Header : BEGIN -->
	        <!-- Email Header : END -->

            <!-- Hero Image, Flush : BEGIN -->
            
       <td>
    <div style="margin: 0 auto; width: 400px">             
    <a href="https://riseconf.com" class="hero-branding">
        <img src = "https://s3-eu-west-1.amazonaws.com/ds-ajm-emails/RISE_Logo_Colour.jpg" alt = "RISE" align = 'middle' >
        </a>
    </div>
</td>

            <!-- Hero Image, Flush : END -->

            <!-- 1 Column Text + Button : BEGIN -->
            <tr>
                <td style="background-color: #ffffff;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <h1 style="margin: 0 0 10px; font-size: 24px; line-height: 125%; color: #333333; font-weight: normal;">Your talk from RISE is now live</h1>
                                <p style="margin: 0 0 10px;">Please find the link to your talk at the button below.</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 0 20px 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <!-- Button : BEGIN -->
                                <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: auto;">
                                    <tr>
                                        <td class="button-td button-td-primary" style="border-radius: 4px; background: #222222;">""" 
    
    html_email_2 =				    """<a class="button-a button-a-primary" href="{}" style="background: #EF4343;; border: 1px solid #EF4343;; font-family: sans-serif; font-size: 15px; line-height: 15px; text-decoration: none; padding: 13px 17px; display: block; border-radius: 4px;"><span class="button-link" style="color:#ffffff">Talk Video</span></a>"""
									
    html_email_3 =              """                  	</td>
                                    </tr>
                                </table>
								<!-- Button : END -->
								<p style="margin: 10 0 10px;"> Your RISE talk can be found at this link: <a href="{}">{}</a>. We do ask that you include "© RISE conf" or "courtesy of RISE conf" when posting your videos online. If you would like to tag our accounts in your video posts on social media our accounts are - Twitter <a href="https://twitter.com/riseconfhq">https://twitter.com/riseconfhq</a>, Facebook <a href = "https://www.facebook.com/RISEConfHQ/">https://www.facebook.com/RISEConfHQ/</a> and Instagram <a href = "https://www.instagram.com/riseconfhq/">https://www.instagram.com/riseconfhq/</a>. We can then share this post on our accounts to our online audience. We also recommend that you use the hashtag #RISEConf to ensure your post reaches the attendees from the event.</p>
                            </td>
                        </tr>
                                """
    html_email_4 = """                </table>
                </td>
            </tr>
            <!-- 1 Column Text + Button : END -->

        <!-- Clear Spacer : BEGIN -->
	        <tr>
	            <td aria-hidden="true" height="40" style="font-size: 0; line-height: 0;">
	                &nbsp;
	            </td>
	        </tr>
	        <!-- Clear Spacer : END -->

	    </table>
	    <!-- Email Body : END -->


		<!--[if mso | IE]>
    </td>
    </tr>
    </table>
    <![endif]-->
    </center>
</body>
</html>

"""
    return  html_email_1 + html_email_2.format(youtube_url) + html_email_3.format(youtube_url, youtube_url) + html_email_4


def html_email_processing_5(youtube_link, vimeo_link,s3_link):
    html_email_1 = """
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->

    <!-- Web Font / @font-face : BEGIN -->
    <!-- NOTE: If web fonts are not required, lines 10 - 27 can be safely removed. -->

    <!-- Desktop Outlook chokes on web font references and defaults to Times New Roman, so we force a safe fallback font. -->
    <!--[if mso]>
        <style>
            * {
                font-family: sans-serif !important;
            }
        </style>
    <![endif]-->

    <!-- All other clients get the webfont reference; some will render the font and others will silently fail to the fallbacks. More on that here: http://stylecampaign.com/blog/2015/02/webfont-support-in-email/ -->
    <!--[if !mso]><!-->
    <!-- insert web font reference, eg: <link href='https://fonts.googleapis.com/css?family=Roboto:400,700' rel='stylesheet' type='text/css'> -->
    <!--<![endif]-->

    <!-- Web Font / @font-face : END -->

    <!-- CSS Reset : BEGIN -->
    <style>

        /* What it does: Remove spaces around the email design added by some email clients. */
        /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */
        html,
        body {
            margin: 0 auto !important;
            padding: 0 !important;
            height: 100% !important;
            width: 100% !important;
        }

        /* What it does: Stops email clients resizing small text. */
        * {
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%;
        }

        /* What it does: Centers email on Android 4.4 */
        div[style*="margin: 16px 0"] {
            margin: 0 !important;
        }

        /* What it does: Stops Outlook from adding extra spacing to tables. */
        table,
        td {
            mso-table-lspace: 0pt !important;
            mso-table-rspace: 0pt !important;
        }

        /* What it does: Fixes webkit padding issue. Fix for Yahoo mail table alignment bug. Applies table-layout to the first 2 tables then removes for anything nested deeper. */
        table {
            border-spacing: 0 !important;
            border-collapse: collapse !important;
            table-layout: fixed !important;
            margin: 0 auto !important;
        }
        table table table {
            table-layout: auto;
        }

        /* What it does: Uses a better rendering method when resizing images in IE. */
        img {
            -ms-interpolation-mode:bicubic;
        }

        /* What it does: A work-around for email clients meddling in triggered links. */
        *[x-apple-data-detectors],  /* iOS */
        .unstyle-auto-detected-links *,
        .aBn {
            border-bottom: 0 !important;
            cursor: default !important;
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }

        /* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
        .a6S {
           display: none !important;
           opacity: 0.01 !important;
       }
       /* If the above doesn't work, add a .g-img class to any image in question. */
       img.g-img + div {
           display: none !important;
       }

       /* What it does: Prevents underlining the button text in Windows 10 */
        .button-link {
            text-decoration: none !important;
        }

        /* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
        /* Create one of these media queries for each additional viewport size you'd like to fix */

        /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
        @media only screen and (min-device-width: 320px) and (max-device-width: 374px) {
            .email-container {
                min-width: 320px !important;
            }
        }
        /* iPhone 6, 6S, 7, 8, and X */
        @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
            .email-container {
                min-width: 375px !important;
            }
        }
        /* iPhone 6+, 7+, and 8+ */
        @media only screen and (min-device-width: 414px) {
            .email-container {
                min-width: 414px !important;
            }
        }

    </style>
    <!-- CSS Reset : END -->
	<!-- Reset list spacing because Outlook ignores much of our inline CSS. -->
	<!--[if mso]>
	<style type="text/css">
		ul,
		ol {
			margin: 0 !important;
		}
		li {
			margin-left: 30px !important;
		}
		li.list-item-first {
			margin-top: 0 !important;
		}
		li.list-item-last {
			margin-bottom: 10px !important;
		}
	</style>
	<![endif]-->

    <!-- Progressive Enhancements : BEGIN -->
    <style>

        /* What it does: Hover styles for buttons */
        .button-td,
        .button-a {
            transition: all 100ms ease-in;
        }
	    .button-td-primary:hover,
	    .button-a-primary:hover {
	        background: #555555 !important;
	        border-color: #555555 !important;
	    }

        /* Media Queries */
        @media screen and (max-width: 600px) {

            .email-container {
                width: 100% !important;
                margin: auto !important;
            }

            /* What it does: Forces elements to resize to the full width of their container. Useful for resizing images beyond their max-width. */
            .fluid {
                max-width: 100% !important;
                height: auto !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            /* What it does: Forces table cells into full-width rows. */
            .stack-column,
            .stack-column-center {
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                direction: ltr !important;
            }
            /* And center justify these ones. */
            .stack-column-center {
                text-align: center !important;
            }

            /* What it does: Generic utility class for centering. Useful for images, buttons, and nested tables. */
            .center-on-narrow {
                text-align: center !important;
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
                float: none !important;
            }
            table.center-on-narrow {
                display: inline-block !important;
            }

            /* What it does: Adjust typography on small screens to improve readability */
            .email-container p {
                font-size: 17px !important;
            }
        }

    </style>
    <!-- Progressive Enhancements : END -->

    <!-- What it does: Makes background images in 72ppi Outlook render at correct size. -->
    <!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->

</head>
<!--
	The email background color (#222222) is defined in three places:
	1. body tag: for most email clients
	2. center tag: for Gmail and Inbox mobile apps and web versions of Gmail, GSuite, Inbox, Yahoo, AOL, Libero, Comcast, freenet, Mail.ru, Orange.fr
	3. mso conditional: For Windows 10 Mail
-->
<body width="100%" style="margin: 0; mso-line-height-rule: exactly; background-color: #ffffff;">
    <center style="width: 100%; background-color: #ffffff; text-align: left;">
    <!--[if mso | IE]>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #222222;">
    <tr>
    <td>
    <![endif]-->

        <!-- Visually Hidden Preheader Text : BEGIN -->
        <!-- Visually Hidden Preheader Text : END -->

        <!-- Create white space after the desired preview text so email clients don’t pull other distracting text into the inbox preview. Extend as necessary. -->
        <!-- Preview Text Spacing Hack : BEGIN -->
        <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
	        &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
        </div>
        <!-- Preview Text Spacing Hack : END -->

        <!-- Email Body : BEGIN -->
        <table align="center" role="presentation" cellspacing="0" cellpadding="10" border="0" width="600" style="margin: 0 auto;" class="email-container">
	        <!-- Email Header : BEGIN -->
	        <!-- Email Header : END -->

            <!-- Hero Image, Flush : BEGIN -->
            
       <td>
    <div style="margin: 0 auto; width: 400px">             
    <a href="https://websummit.com" class="hero-branding">
        <img src = "https://s3-eu-west-1.amazonaws.com/ds-ajm-emails/Web_Summit_Logo_Stacked_Colour.jpg" alt = "WebSummit" align = 'middle' >
        </a>
    </div>
</td>

            <!-- Hero Image, Flush : END -->

            <!-- 1 Column Text + Button : BEGIN -->
            <tr>
                <td style="background-color: #ffffff;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <h1 style="margin: 0 0 10px; font-size: 24px; line-height: 125%; color: #333333; font-weight: normal;">Your talk from WebSummit is now live</h1>
                                <p style="margin: 0 0 10px;">Please find the link to your talk at the button below.</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 0 20px 20px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                <!-- Button : BEGIN -->
                                <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: auto;">
                                    <tr>
                                        <td class="button-td button-td-primary" style="border-radius: 4px; background: #ffffff;">""" 
    
    html_email_2 =				    """<a class="button-a button-a-primary" href="{}" style="margin:10px;background: #E90D7F;; border: 1px solid #EF4343;; font-family: sans-serif; font-size: 15px; line-height: 15px; text-decoration: none; padding: 13px 17px; display: block; border-radius: 4px;"><span class="button-link" style="color:#ffffff">Vimeo link</span></a>"""


    html_email_3 =				    """<a class="button-a button-a-primary" href="{}" style="margin:10px; background: #E90D7F; border: 1px solid #EF4343;; font-family: sans-serif; font-size: 15px; line-height: 15px; text-decoration: none; padding: 13px 17px; display: block; border-radius: 4px;"><span class="button-link" style="color:#ffffff">Download link</span></a>"""

    html_email_4 =              """                  	</td>
                                    </tr>
                                </table>
								<!-- Button : END -->
								<p style="margin: 10 0 10px;align="justify"> Your WebSummit talk can be found at this link: <a href="{}">{}</a>. We do ask that you include "© WebSummit" or "courtesy of WebSummit" when posting your videos online. If you would like to tag our accounts in your video posts on social media our accounts are - Twitter <a href="https://twitter.com/websummit">https://twitter.com/websummit</a>, Facebook <a href = "https://www.facebook.com/WebSummitHQ/">https://www.facebook.com/WebSummitHQ/</a> and Instagram <a href = "https://www.instagram.com/websummit/">https://www.instagram.com/websummit/</a>. We can then share this post on our accounts to our online audience. We also recommend that you use the hashtag #WebSummit to ensure your post reaches the attendees from the event.</p>
                            </td>
                        </tr>
                                """
    html_email_5 = """                </table>
                </td>
            </tr>
            <!-- 1 Column Text + Button : END -->

        <!-- Clear Spacer : BEGIN -->
	        <tr>
	            <td aria-hidden="true" height="40" style="font-size: 0; line-height: 0;">
	                &nbsp;
	            </td>
	        </tr>
	        <!-- Clear Spacer : END -->

	    </table>
	    <!-- Email Body : END -->


		<!--[if mso | IE]>
    </td>
    </tr>
    </table>
    <![endif]-->
    </center>
</body>
</html>

"""
    return  html_email_1 + html_email_2.format(vimeo_link) + html_email_3.format(s3_link) + html_email_4.format(vimeo_link, vimeo_link) + html_email_5



if __name__ == '__main__':
    #out = html_email_processing_4('WebSummit','youtube.com')
    out = html_email_processing_5('youtube.com', 'vimeo.com','s3_link.com')
    with open('HTML_WS19.html','w') as f:
        f.write(out)