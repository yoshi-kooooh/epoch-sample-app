FROM	nginx

WORKDIR /app

COPY ./ui-app /app

RUN	echo	"server {"		        	        >	/etc/nginx/conf.d/epochui.conf \
&&	echo	"  listen    8000;"		                >>	/etc/nginx/conf.d/epochui.conf \
&&	echo	"  location  / {"		                >>	/etc/nginx/conf.d/epochui.conf \
&&	echo	"    root /app;"				>>	/etc/nginx/conf.d/epochui.conf \
&&	echo	"  }"				                >>	/etc/nginx/conf.d/epochui.conf \
&&	echo	"}"				                >>	/etc/nginx/conf.d/epochui.conf \
