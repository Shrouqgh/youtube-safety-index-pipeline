# Project Progress Log

## Week 1 (Oct 1 - Oct 7)
- **Hours Worked**: 9
- **Tasks Completed**:
  - Installed Ubuntu ISO image on a virtual machine 
  - Installed Squid and configured the proxy settings
  - Ran into issues with SSL support—faced challenges understanding how SSL bumping works with Squid.
  - Spent some  time troubleshooting the `sslcrtd_program` helper crashes. Tried several approaches related to permissions on the certificate directories.
  - Generated a certificate for SSL bumping and imported it to the client device (iPhone) to allow/test SSL interception.
  - Configured basic proxy functionality but couldn't get SSL certificates working properly yet.
  - No successful test results logged from the phone setup,possibly due to iOS privacy restrictions or security features. more work is needed to capture the logs.

## Week 2 (Oct 8 - Oct 14)
- **Hours Worked**: 4
- **Tasks Completed**:
  - Continued working on fixing the SSL helper crash issue - focused on permission configurations and rebuilding the SSL database.
  - Ran further tests on the proxy setup with the iPhone, but logs weren’t generated, suggesting further issues with SSL interception or configuration.
  - Checked port conflicts and verified cache settings, but the root cause of the SSL crash still  unresolved.
  - Next step: explore alternative solutions for resolving SSL certificate generation and ensuring Squid captures client traffic. will utilize Windows OS as a client.

