FROM coffeateam/coffea-casa:0.4.1

RUN pip install --ignore-installed --no-cache-dir \
    git+git://github.com/mat-adamec/coffea-casa.git@master#egg=coffea_casa
    
USER root 
ADD prepare-env.sh /usr/local/bin/
RUN chmod ugo+x /usr/local/bin/prepare-env.sh