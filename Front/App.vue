<script>
	export default {
		globalData: {
			token: 'token',
		},
		onLaunch: function() {
			console.log('App Launch');
			var get_token_json = {
				"username": "admin",
				"pwd": "admin"
			};
			uni.request({
				url: this.$host + '/api/auth/token/',
				data: get_token_json,
				header:{'content-type':'application/json'},
				method: 'POST',
				success: (result) => {
					uni.setStorage({
						key: 'access_token',
						data: result.data['data']['access_token']
					})
				},
				fail: (err) => {
					console.log(err);
				},
			})
			// #ifdef APP-NVUE
			plus.screen.lockOrientation('portrait-primary');
			let appid = plus.runtime.appid;
			if (appid && appid.toLocaleLowerCase() != "hbuilder") {
				uni.request({
					url: 'https://uniapp.dcloud.io/update', //检查更新的服务器地址
					data: {
						appid: plus.runtime.appid,
						version: plus.runtime.version
					},
					success: (res) => {
						console.log('success', res);
						if (res.statusCode == 200 && res.data.isUpdate) {
							let openUrl = plus.os.name === 'iOS' ? res.data.iOS : res.data.Android;
							// 提醒用户更新
							uni.showModal({
								title: '更新提示',
								content: res.data.note ? res.data.note : '是否选择更新',
								success: (showResult) => {
									if (showResult.confirm) {
										plus.runtime.openURL(openUrl);
									}
								}
							})
						}
					}
				})
			}

			var domModule = weex.requireModule('dom');
			domModule.addRule('fontFace', {
				'fontFamily': "texticons",
				'src': "url('./static/text-icon.ttf')"
			});
			// #endif
		},
		onShow: function() {
			console.log('App Show');
			const storage_token = uni.getStorageSync('access_token');
			this.globalData.token = storage_token;
		},
		onHide: function() {
			console.log('App Hide')
		},
	}
</script>

<style>
	/*每个页面公共css */
</style>
