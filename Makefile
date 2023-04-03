.PHONY: package
package: dev-package
	cp ./manifest.txt /tmp/final_package
	cp ./CrowdSec.xml /tmp/final_package

	cd /tmp/final_package && zip -r CrowdSec.zip ./  
	cp /tmp/final_package/CrowdSec.zip ./
	

.PHONY: sign
sign:
	jarsigner -keystore signingstore.jks -storepass "$(STORE_PASS)" -tsa http://timestamp.digicert.com CrowdSec.zip "codesigningcert"
	jarsigner -keystore signingstore_old.jks -storepass "$(STORE_PASS)" -tsa http://timestamp.digicert.com -sigfile oldcert CrowdSec.zip "codesigningcert"

.PHONY: clean
clean:
	rm -rf /tmp/final_package > /dev/null
	rm -rf /tmp/package > /dev/null

.PHONY: dev-package
dev-package: clean
	mkdir /tmp/package/
	mkdir -p /tmp/final_package/CrowdSec

	cp -r ./app /tmp/package/
	cp -r ./container /tmp/package/
	cp ./manifest.json /tmp/package/
	cd /tmp/package && zip -r /tmp/final_package/CrowdSec/1124.zip ./
	cp /tmp/final_package/CrowdSec/1124.zip ./
