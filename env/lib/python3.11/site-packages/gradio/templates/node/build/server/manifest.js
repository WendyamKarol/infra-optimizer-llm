const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.A1rjDn0t.js","app":"_app/immutable/entry/app.DRdDsZ41.js","imports":["_app/immutable/entry/start.A1rjDn0t.js","_app/immutable/chunks/client.BU6TeQdu.js","_app/immutable/entry/app.DRdDsZ41.js","_app/immutable/chunks/preload-helper.DpQnamwV.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-B7h5KJLT.js')),
			__memo(() => import('./chunks/1-NOyM39Tl.js')),
			__memo(() => import('./chunks/2-Bcd_Tkvz.js').then(function (n) { return n.aD; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
